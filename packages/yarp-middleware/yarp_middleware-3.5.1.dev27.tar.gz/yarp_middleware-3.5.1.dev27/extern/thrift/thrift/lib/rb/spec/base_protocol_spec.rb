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

require 'spec_helper'

describe 'BaseProtocol' do

  before(:each) do
    @trans = double("MockTransport")
    @prot = Thrift::BaseProtocol.new(@trans)
  end

  describe Thrift::BaseProtocol do
    # most of the methods are stubs, so we can ignore them

    it "should provide a reasonable to_s" do
      expect(@trans).to receive(:to_s).once.and_return("trans")
      expect(@prot.to_s).to eq("trans")
    end

    it "should make trans accessible" do
      expect(@prot.trans).to eql(@trans)
    end

    it 'should write out a field nicely (deprecated write_field signature)' do
      expect(@prot).to receive(:write_field_begin).with('field', 'type', 'fid').ordered
      expect(@prot).to receive(:write_type).with({:name => 'field', :type => 'type'}, 'value').ordered
      expect(@prot).to receive(:write_field_end).ordered
      @prot.write_field('field', 'type', 'fid', 'value')
    end

    it 'should write out a field nicely' do
      expect(@prot).to receive(:write_field_begin).with('field', 'type', 'fid').ordered
      expect(@prot).to receive(:write_type).with({:name => 'field', :type => 'type', :binary => false}, 'value').ordered
      expect(@prot).to receive(:write_field_end).ordered
      @prot.write_field({:name => 'field', :type => 'type', :binary => false}, 'fid', 'value')
    end

    it 'should write out the different types (deprecated write_type signature)' do
      expect(@prot).to receive(:write_bool).with('bool').ordered
      expect(@prot).to receive(:write_byte).with('byte').ordered
      expect(@prot).to receive(:write_double).with('double').ordered
      expect(@prot).to receive(:write_i16).with('i16').ordered
      expect(@prot).to receive(:write_i32).with('i32').ordered
      expect(@prot).to receive(:write_i64).with('i64').ordered
      expect(@prot).to receive(:write_string).with('string').ordered
      struct = double('Struct')
      expect(struct).to receive(:write).with(@prot).ordered
      @prot.write_type(Thrift::Types::BOOL, 'bool')
      @prot.write_type(Thrift::Types::BYTE, 'byte')
      @prot.write_type(Thrift::Types::DOUBLE, 'double')
      @prot.write_type(Thrift::Types::I16, 'i16')
      @prot.write_type(Thrift::Types::I32, 'i32')
      @prot.write_type(Thrift::Types::I64, 'i64')
      @prot.write_type(Thrift::Types::STRING, 'string')
      @prot.write_type(Thrift::Types::STRUCT, struct)
      # all other types are not implemented
      [Thrift::Types::STOP, Thrift::Types::VOID, Thrift::Types::MAP, Thrift::Types::SET, Thrift::Types::LIST].each do |type|
        expect { @prot.write_type(type, type.to_s) }.to raise_error(NotImplementedError)
      end
    end

    it 'should write out the different types' do
      expect(@prot).to receive(:write_bool).with('bool').ordered
      expect(@prot).to receive(:write_byte).with('byte').ordered
      expect(@prot).to receive(:write_double).with('double').ordered
      expect(@prot).to receive(:write_i16).with('i16').ordered
      expect(@prot).to receive(:write_i32).with('i32').ordered
      expect(@prot).to receive(:write_i64).with('i64').ordered
      expect(@prot).to receive(:write_string).with('string').ordered
      expect(@prot).to receive(:write_binary).with('binary').ordered
      struct = double('Struct')
      expect(struct).to receive(:write).with(@prot).ordered
      @prot.write_type({:type => Thrift::Types::BOOL}, 'bool')
      @prot.write_type({:type => Thrift::Types::BYTE}, 'byte')
      @prot.write_type({:type => Thrift::Types::DOUBLE}, 'double')
      @prot.write_type({:type => Thrift::Types::I16}, 'i16')
      @prot.write_type({:type => Thrift::Types::I32}, 'i32')
      @prot.write_type({:type => Thrift::Types::I64}, 'i64')
      @prot.write_type({:type => Thrift::Types::STRING}, 'string')
      @prot.write_type({:type => Thrift::Types::STRING, :binary => true}, 'binary')
      @prot.write_type({:type => Thrift::Types::STRUCT}, struct)
      # all other types are not implemented
      [Thrift::Types::STOP, Thrift::Types::VOID, Thrift::Types::MAP, Thrift::Types::SET, Thrift::Types::LIST].each do |type|
        expect { @prot.write_type({:type => type}, type.to_s) }.to raise_error(NotImplementedError)
      end
    end

    it 'should read the different types (deprecated read_type signature)' do
      expect(@prot).to receive(:read_bool).ordered
      expect(@prot).to receive(:read_byte).ordered
      expect(@prot).to receive(:read_i16).ordered
      expect(@prot).to receive(:read_i32).ordered
      expect(@prot).to receive(:read_i64).ordered
      expect(@prot).to receive(:read_double).ordered
      expect(@prot).to receive(:read_string).ordered
      @prot.read_type(Thrift::Types::BOOL)
      @prot.read_type(Thrift::Types::BYTE)
      @prot.read_type(Thrift::Types::I16)
      @prot.read_type(Thrift::Types::I32)
      @prot.read_type(Thrift::Types::I64)
      @prot.read_type(Thrift::Types::DOUBLE)
      @prot.read_type(Thrift::Types::STRING)
      # all other types are not implemented
      [Thrift::Types::STOP, Thrift::Types::VOID, Thrift::Types::MAP,
       Thrift::Types::SET, Thrift::Types::LIST, Thrift::Types::STRUCT].each do |type|
        expect { @prot.read_type(type) }.to raise_error(NotImplementedError)
      end
    end

    it 'should read the different types' do
      expect(@prot).to receive(:read_bool).ordered
      expect(@prot).to receive(:read_byte).ordered
      expect(@prot).to receive(:read_i16).ordered
      expect(@prot).to receive(:read_i32).ordered
      expect(@prot).to receive(:read_i64).ordered
      expect(@prot).to receive(:read_double).ordered
      expect(@prot).to receive(:read_string).ordered
      expect(@prot).to receive(:read_binary).ordered
      @prot.read_type({:type => Thrift::Types::BOOL})
      @prot.read_type({:type => Thrift::Types::BYTE})
      @prot.read_type({:type => Thrift::Types::I16})
      @prot.read_type({:type => Thrift::Types::I32})
      @prot.read_type({:type => Thrift::Types::I64})
      @prot.read_type({:type => Thrift::Types::DOUBLE})
      @prot.read_type({:type => Thrift::Types::STRING})
      @prot.read_type({:type => Thrift::Types::STRING, :binary => true})
      # all other types are not implemented
      [Thrift::Types::STOP, Thrift::Types::VOID, Thrift::Types::MAP,
       Thrift::Types::SET, Thrift::Types::LIST, Thrift::Types::STRUCT].each do |type|
        expect { @prot.read_type({:type => type}) }.to raise_error(NotImplementedError)
      end
    end

    it "should skip the basic types" do
      expect(@prot).to receive(:read_bool).ordered
      expect(@prot).to receive(:read_byte).ordered
      expect(@prot).to receive(:read_i16).ordered
      expect(@prot).to receive(:read_i32).ordered
      expect(@prot).to receive(:read_i64).ordered
      expect(@prot).to receive(:read_double).ordered
      expect(@prot).to receive(:read_string).ordered
      @prot.skip(Thrift::Types::BOOL)
      @prot.skip(Thrift::Types::BYTE)
      @prot.skip(Thrift::Types::I16)
      @prot.skip(Thrift::Types::I32)
      @prot.skip(Thrift::Types::I64)
      @prot.skip(Thrift::Types::DOUBLE)
      @prot.skip(Thrift::Types::STRING)
    end

    it "should skip structs" do
      real_skip = @prot.method(:skip)
      expect(@prot).to receive(:read_struct_begin).ordered
      expect(@prot).to receive(:read_field_begin).exactly(4).times.and_return(
        ['field 1', Thrift::Types::STRING, 1],
        ['field 2', Thrift::Types::I32, 2],
        ['field 3', Thrift::Types::MAP, 3],
        [nil, Thrift::Types::STOP, 0]
      )
      expect(@prot).to receive(:read_field_end).exactly(3).times
      expect(@prot).to receive(:read_string).exactly(3).times
      expect(@prot).to receive(:read_i32).ordered
      expect(@prot).to receive(:read_map_begin).ordered.and_return([Thrift::Types::STRING, Thrift::Types::STRING, 1])
      # @prot.should_receive(:read_string).exactly(2).times
      expect(@prot).to receive(:read_map_end).ordered
      expect(@prot).to receive(:read_struct_end).ordered
      real_skip.call(Thrift::Types::STRUCT)
    end

    it "should skip maps" do
      real_skip = @prot.method(:skip)
      expect(@prot).to receive(:read_map_begin).ordered.and_return([Thrift::Types::STRING, Thrift::Types::STRUCT, 1])
      expect(@prot).to receive(:read_string).ordered
      expect(@prot).to receive(:read_struct_begin).ordered.and_return(["some_struct"])
      expect(@prot).to receive(:read_field_begin).ordered.and_return([nil, Thrift::Types::STOP, nil]);
      expect(@prot).to receive(:read_struct_end).ordered
      expect(@prot).to receive(:read_map_end).ordered
      real_skip.call(Thrift::Types::MAP)
    end

    it "should skip sets" do
      real_skip = @prot.method(:skip)
      expect(@prot).to receive(:read_set_begin).ordered.and_return([Thrift::Types::I64, 9])
      expect(@prot).to receive(:read_i64).ordered.exactly(9).times
      expect(@prot).to receive(:read_set_end)
      real_skip.call(Thrift::Types::SET)
    end

    it "should skip lists" do
      real_skip = @prot.method(:skip)
      expect(@prot).to receive(:read_list_begin).ordered.and_return([Thrift::Types::DOUBLE, 11])
      expect(@prot).to receive(:read_double).ordered.exactly(11).times
      expect(@prot).to receive(:read_list_end)
      real_skip.call(Thrift::Types::LIST)
    end
  end

  describe Thrift::BaseProtocolFactory do
    it "should raise NotImplementedError" do
      # returning nil since Protocol is just an abstract class
      expect {Thrift::BaseProtocolFactory.new.get_protocol(double("MockTransport"))}.to raise_error(NotImplementedError)
    end

    it "should provide a reasonable to_s" do
      expect(Thrift::BaseProtocolFactory.new.to_s).to eq("base")
    end
  end
end
