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

module Thrift
  class BaseServer
    def initialize(processor, server_transport, transport_factory=nil, protocol_factory=nil)
      @processor = processor
      @server_transport = server_transport
      @transport_factory = transport_factory ? transport_factory : Thrift::BaseTransportFactory.new
      @protocol_factory = protocol_factory ? protocol_factory : Thrift::BinaryProtocolFactory.new
    end

    def serve
      raise NotImplementedError
    end

    def to_s
      "server(#{@protocol_factory.to_s}(#{@transport_factory.to_s}(#{@server_transport.to_s})))"
    end
  end
end
