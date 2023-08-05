#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


@compiles(BigInteger, 'sqlite')
def bi_c(element, compiler, **kw):
    return "INTEGER"


class Base:
    __table_args__ = {'sqlite_autoincrement': True}

    """
    Column uuid is SQL model primary key, auto increment, which type is BigInteger, but Integer for SQLite.
    """
    uuid = Column(BigInteger, primary_key=True, autoincrement=True)
