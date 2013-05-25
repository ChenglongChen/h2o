import os, json, unittest, time, shutil, sys
sys.path.extend(['.','..','py'])
import h2o, h2o_cmd,h2o_hosts, h2o_browse as h2b, h2o_import as h2i, h2o_hosts
import time, random

class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        global localhost
        localhost = h2o.decide_if_localhost()
        if (localhost):
            h2o.build_cloud(1,java_heap_GB=10)
        else:
            h2o_hosts.build_cloud_with_hosts(1,java_heap_GB=10)

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_from_import(self):
        importFolderPath = '/home/0xdiag/datasets/standard'
        h2i.setupImportFolder(None, importFolderPath)
        timeoutSecs = 500
        csvFilenameAll = [
            "covtype.data",
            "covtype20x.data",
            # "covtype200x.data",
            # "100million_rows.csv",
            # "200million_rows.csv",
            # "a5m.csv",
            # "a10m.csv",
            # "a100m.csv",
            # "a200m.csv",
            # "a400m.csv",
            # "a600m.csv",
            # "billion_rows.csv.gz",
            # "new-poker-hand.full.311M.txt.gz",
            ]
        # csvFilenameList = random.sample(csvFilenameAll,1)
        csvFilenameList = csvFilenameAll

        # pop open a browser on the cloud
        h2b.browseTheCloud()

        for csvFilename in csvFilenameList:
            # creates csvFilename.hex from file in importFolder dir 
            parseKey = h2i.parseImportFolderFile(None, csvFilename, importFolderPath, timeoutSecs=500)
            print csvFilename, 'parse time:', parseKey['response']['time']
            print "Parse result['destination_key']:", parseKey['destination_key']
            inspect = h2o_cmd.runInspect(key=parseKey['destination_key'])

            print "\n" + csvFilename
            start = time.time()
            RFview = h2o_cmd.runRFOnly(trees=1,depth=25,parseKey=parseKey,
                timeoutSecs=timeoutSecs)

            h2b.browseJsonHistoryAsUrlLastMatch("RFView")
            time.sleep(10)

            sys.stdout.write('.')
            sys.stdout.flush() 

if __name__ == '__main__':
    h2o.unit_main()
