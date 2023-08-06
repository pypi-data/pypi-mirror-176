# Copyright (c) 2022, Eric Lemoine
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


class EngineIOError(Exception):
    pass


class EngineIoConnectionError(EngineIOError):
    pass
