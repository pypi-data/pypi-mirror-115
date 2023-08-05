/*
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
 */

#ifndef _THRIFT_TNAME_ME_H_
#define _THRIFT_TNAME_ME_H_ 1

#include <thrift/async/TAsyncProcessor.h>
#include <thrift/async/TAsyncBufferProcessor.h>
#include <thrift/protocol/TProtocol.h>

namespace apache {
namespace thrift {
namespace async {

class TAsyncProtocolProcessor : public TAsyncBufferProcessor {
public:
  TAsyncProtocolProcessor(std::shared_ptr<TAsyncProcessor> underlying,
                          std::shared_ptr<apache::thrift::protocol::TProtocolFactory> pfact)
    : underlying_(underlying), pfact_(pfact) {}

  void process(std::function<void(bool healthy)> _return,
                       std::shared_ptr<apache::thrift::transport::TBufferBase> ibuf,
                       std::shared_ptr<apache::thrift::transport::TBufferBase> obuf) override;

  ~TAsyncProtocolProcessor() override = default;

private:
  static void finish(std::function<void(bool healthy)> _return,
                     std::shared_ptr<apache::thrift::protocol::TProtocol> oprot,
                     bool healthy);

  std::shared_ptr<TAsyncProcessor> underlying_;
  std::shared_ptr<apache::thrift::protocol::TProtocolFactory> pfact_;
};
}
}
} // apache::thrift::async

#endif // #ifndef _THRIFT_TNAME_ME_H_
