# Copyright (c) 2016, MD2K Center of Excellence
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import uuid

import cerebralcortex
from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.kernel.datatypes.datastream import DataStream
from cerebralcortex.legacy import find
from memphisdataprocessor.cStress import cStress
from memphisdataprocessor.preprocessor import parser

CC = cerebralcortex.CerebralCortex(master="local[*]", name="Memphis cStress Development App")

basedir = "/Users/hnat/Desktop/data/"

for i in range(1, 2):
    participant = "SI%02d" % i

    participant_UUID = uuid.uuid4()
    try:
        ecgRDD = CC.readfile(find(basedir, {"participant": participant, "datasource": "ecg"})).map(
            parser.dataprocessor).filter(lambda x: isinstance(x, DataPoint))
        ecgRDD.persist()
        ecg = DataStream(participant_UUID, data=ecgRDD)

        ripRDD = CC.readfile(find(basedir, {"participant": participant, "datasource": "rip"})).map(
            parser.dataprocessor).filter(lambda x: isinstance(x, DataPoint))
        ripRDD.persist()
        rip = DataStream(participant_UUID, data=ripRDD)

        accelxRDD = CC.readfile(find(basedir, {"participant": participant, "datasource": "accelx"})).map(
            parser.dataprocessor).filter(lambda x: isinstance(x, DataPoint))
        accelxRDD.persist()
        accelx = DataStream(participant_UUID, data=accelxRDD)

        accelyRDD = CC.readfile(find(basedir, {"participant": participant, "datasource": "accely"})).map(
            parser.dataprocessor).filter(lambda x: isinstance(x, DataPoint))
        accelyRDD.persist()
        accely = DataStream(participant_UUID, data=accelyRDD)

        accelzRDD = CC.readfile(find(basedir, {"participant": participant, "datasource": "accelz"})).map(
            parser.dataprocessor).filter(lambda x: isinstance(x, DataPoint))
        accelzRDD.persist()
        accelz = DataStream(participant_UUID, data=accelzRDD)

        cStressFeatures = cStress(ecg, rip, accelx, accely, accelz)

        # resultPuff = puffMarker(CC, rip, accelx, accely, accelz, lwAccel, lwGyro, rwAccel, rwGyro)

        # print(participant, participant_UUID, cStressFeatures.get_datapoints().count())
    except Exception as e:
        print("File missing for %s" % participant)
        print(e)
