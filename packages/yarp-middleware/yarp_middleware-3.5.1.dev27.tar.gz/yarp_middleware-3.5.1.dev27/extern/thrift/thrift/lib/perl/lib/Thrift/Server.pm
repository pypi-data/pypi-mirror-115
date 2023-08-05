#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

use 5.10.0;
use strict;
use warnings;

use Thrift;
use Thrift::BinaryProtocol;
use Thrift::BufferedTransport;
use Thrift::Exception;

#
# Server base class module
#
package Thrift::Server;
use version 0.77; our $VERSION = version->declare("$Thrift::VERSION");

#
# 3 possible constructors:
#   1.  (processor, serverTransport)
#       Uses a BufferedTransportFactory and a BinaryProtocolFactory.
#   2.  (processor, serverTransport, transportFactory, protocolFactory)
#       Uses the same factory for input and output of each type.
#   3.  (processor, serverTransport,
#        inputTransportFactory, outputTransportFactory,
#        inputProtocolFactory, outputProtocolFactory)
#
sub new
{
    my $classname    = shift;
    my @args         = @_;

    my $self;

    if (scalar @args == 2)
    {
        $self = _init($args[0], $args[1],
                    Thrift::BufferedTransportFactory->new(),
                    Thrift::BufferedTransportFactory->new(),
                    Thrift::BinaryProtocolFactory->new(),
                    Thrift::BinaryProtocolFactory->new());
    }
    elsif (scalar @args == 4)
    {
      $self = _init($args[0], $args[1], $args[2], $args[2], $args[3], $args[3]);
    }
    elsif (scalar @args == 6)
    {
      $self = _init($args[0], $args[1], $args[2], $args[3], $args[4], $args[5]);
    }
    else
    {
      die Thrift::TException->new('Thrift::Server expects exactly 2, 4, or 6 args');
    }

    return bless($self,$classname);
}

sub _init
{
    my $processor              = shift;
    my $serverTransport        = shift;
    my $inputTransportFactory  = shift;
    my $outputTransportFactory = shift;
    my $inputProtocolFactory   = shift;
    my $outputProtocolFactory  = shift;

    my $self = {
        processor              => $processor,
        serverTransport        => $serverTransport,
        inputTransportFactory  => $inputTransportFactory,
        outputTransportFactory => $outputTransportFactory,
        inputProtocolFactory   => $inputProtocolFactory,
        outputProtocolFactory  => $outputProtocolFactory,
    };
}

sub serve
{
    die 'abstract';
}

sub _clientBegin
{
    my $self  = shift;
    my $iprot = shift;
    my $oprot = shift;

    if (exists  $self->{serverEventHandler} and
        defined $self->{serverEventHandler})
    {
        $self->{serverEventHandler}->clientBegin($iprot, $oprot);
    }
}

sub _handleException
{
    my $self = shift;
    my $e    = shift;

    if ($e->isa('Thrift::TException') and exists $e->{message}) {
        my $message = $e->{message};
        my $code    = $e->{code};
        my $out     = $code . ':' . $message;

        $message =~ m/TTransportException/ and die $out;
        if ($message =~ m/Socket/) {
            # suppress Socket messages
        }
        else {
            warn $out;
        }
    }
    else {
        warn $e;
    }
}

#
# SimpleServer from the Server base class that handles one connection at a time
#
package Thrift::SimpleServer;
use parent -norequire, 'Thrift::Server';
use version 0.77; our $VERSION = version->declare("$Thrift::VERSION");

sub new
{
    my $classname = shift;

    my $self      = $classname->SUPER::new(@_);

    return bless($self,$classname);
}

sub serve
{
    my $self = shift;
    my $stop = 0;

    $self->{serverTransport}->listen();
    while (!$stop) {
        my $client = $self->{serverTransport}->accept();
        if (defined $client) {
            my $itrans = $self->{inputTransportFactory}->getTransport($client);
            my $otrans = $self->{outputTransportFactory}->getTransport($client);
            my $iprot  = $self->{inputProtocolFactory}->getProtocol($itrans);
            my $oprot  = $self->{outputProtocolFactory}->getProtocol($otrans);
            eval {
                $self->_clientBegin($iprot, $oprot);
                while (1)
                {
                    $self->{processor}->process($iprot, $oprot);
                }
            };
            if($@) {
                $self->_handleException($@);
            }
            $itrans->close();
            $otrans->close();
        } else {
            $stop = 1;
        }
    }
}


#
# ForkingServer that forks a new process for each request
#
package Thrift::ForkingServer;
use parent -norequire, 'Thrift::Server';
use POSIX ':sys_wait_h';
use version 0.77; our $VERSION = version->declare("$Thrift::VERSION");

sub new
{
    my $classname = shift;
    my @args      = @_;

    my $self      = $classname->SUPER::new(@args);
    return bless($self,$classname);
}


sub serve
{
    my $self = shift;

    # THRIFT-3848: without ignoring SIGCHLD, perl ForkingServer goes into a tight loop
    $SIG{CHLD} = 'IGNORE';

    $self->{serverTransport}->listen();
    while (1)
    {
        my $client = $self->{serverTransport}->accept();
        $self->_client($client);
    }
}

sub _client
{
    my $self   = shift;
    my $client = shift;

    eval {
        my $itrans = $self->{inputTransportFactory}->getTransport($client);
        my $otrans = $self->{outputTransportFactory}->getTransport($client);

        my $iprot  = $self->{inputProtocolFactory}->getProtocol($itrans);
        my $oprot  = $self->{outputProtocolFactory}->getProtocol($otrans);

        $self->_clientBegin($iprot, $oprot);

        my $pid = fork();

        if ($pid)
        {
            $self->_parent($pid, $itrans, $otrans);
        }
        else {
            $self->_child($itrans, $otrans, $iprot, $oprot);
        }
    };
    if($@) {
        $self->_handleException($@);
    }
}

sub _parent
{
    my $self   = shift;
    my $pid    = shift;
    my $itrans = shift;
    my $otrans = shift;

    # Parent must close socket or the connection may not get closed promptly
    $self->tryClose($itrans);
    $self->tryClose($otrans);
}

sub _child
{
    my $self   = shift;
    my $itrans = shift;
    my $otrans = shift;
    my $iprot  = shift;
    my $oprot  = shift;

    my $ecode = 0;
    eval {
        # THRIFT-4065 ensure child process has normal signal handling in case thrift handler uses it
        $SIG{CHLD} = 'DEFAULT';
        while (1)
        {
            $self->{processor}->process($iprot, $oprot);
        }
    };
    if($@) {
        $ecode = 1;
        $self->_handleException($@);
    }

    $self->tryClose($itrans);
    $self->tryClose($otrans);

    exit($ecode);
}

sub tryClose
{
    my $self = shift;
    my $file = shift;

    eval {
        if (defined $file)
        {
          $file->close();
        }
    };
    if($@) {
        if ($@->isa('Thrift::TException') and exists $@->{message}) {
            my $message = $@->{message};
            my $code    = $@->{code};
            my $out     = $code . ':' . $message;

            warn $out;
        }
        else {
            warn $@;
        }
    }
}

1;
