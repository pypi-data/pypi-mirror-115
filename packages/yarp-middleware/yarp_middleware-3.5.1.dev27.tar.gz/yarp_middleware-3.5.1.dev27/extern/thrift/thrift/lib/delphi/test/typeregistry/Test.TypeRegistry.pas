(*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *)

unit Test.TypeRegistry;

interface

uses
  Classes, SysUtils, TypInfo,
  Thrift,
  Thrift.TypeRegistry,
  DebugProtoTest;


procedure RunTest;


implementation


type
  Tester<T : IInterface> = class
  public
    class procedure Test;
  end;



class procedure Tester<T>.Test;
var instance : T;
    name : string;
begin
  instance := TypeRegistry.Construct<T>;
  name := GetTypeName(TypeInfo(T));
  if instance <> nil
  then Writeln( name, ' = ok')
  else begin
    Writeln( name, ' = failed');
    raise Exception.Create( 'Test with '+name+' failed!');
  end;
end;


procedure RunTest;
begin
  Writeln('Testing type registry ...');

  Tester<IDoubles>.Test;
  Tester<IOneOfEach>.Test;
  Tester<IBonk>.Test;
  Tester<INesting>.Test;
  Tester<IHolyMoley>.Test;
  Tester<IBackwards>.Test;
  Tester<IEmpty>.Test;
  Tester<IWrapper>.Test;
  Tester<IRandomStuff>.Test;
  Tester<IBase64>.Test;
  Tester<ICompactProtoTestStruct>.Test;
  Tester<ISingleMapTestStruct>.Test;
  Tester<IBlowUp>.Test;
  Tester<IReverseOrderStruct>.Test;
  Tester<IStructWithSomeEnum>.Test;
  Tester<ITestUnion>.Test;
  Tester<ITestUnionMinusStringField>.Test;
  Tester<IComparableUnion>.Test;
  Tester<IStructWithAUnion>.Test;
  Tester<IPrimitiveThenStruct>.Test;
  Tester<IStructWithASomemap>.Test;
  Tester<IBigFieldIdStruct>.Test;
  Tester<IBreaksRubyCompactProtocol>.Test;
  Tester<ITupleProtocolTestStruct>.Test;

  Writeln;
end;


end.

