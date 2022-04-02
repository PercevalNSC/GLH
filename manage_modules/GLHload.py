# activitysegmentとplacevisitの親クラス
class ParentGLHSegment:
    def __init__(self, segmentdata):
        self.segmentdict = segmentdata
    
    def convertLatLng (self, latlngset, latlnglist = ['latitudeE7', 'longitudeE7', 'latE7', 'lngE7']):
        offset = 10000000
        for i in latlnglist:
            if i in latlngset :
                latlngset[i] = latlngset[i] / offset
            else:
                pass
        
    def convertTimestamp (self, timestamp):
        return int(timestamp)
    def initDuration (self):
        duration = self.segmentdict['duration']
        for k,v in duration.items():
            duration[k] = self.convertTimestamp(v)
    def initSimplifiedRawPath(self):
        simplifiedRawPath = self.segmentdict['simplifiedRawPath']
        for point in simplifiedRawPath['points']:
            self.convertLatLng(point)
            point['timestampMs'] = self.convertTimestamp(point['timestampMs'])
    def print (self):
        print(self.segmentdict)

class ActivitySegment(ParentGLHSegment):
    def __init__(self, segmentdata):
        super().__init__(segmentdata)
    
    def initActivitySegment(self):
        self.initLocation()
        self.initDuration()
        if "waypointPath" in self.segmentdict:
            self.initWaypointPath()
        if "simplifiedRawPath" in self.segmentdict:
            self.initSimplifiedRawPath()

    def initLocation(self):
        self.convertLatLng(self.segmentdict['startLocation'])
        self.convertLatLng(self.segmentdict['endLocation'])
    def initWaypointPath(self):
        waypointPath = self.segmentdict['waypointPath']
        for i in waypointPath['waypoints']:
            self.convertLatLng(i)
    
class PlaceVisit(ParentGLHSegment):
    def __init__(self, segmentdata):
        super().__init__(segmentdata)

    def initPlaceVisit(self):
        self.initLocation()
        self.initDuration()
        self.initCenter()
        if "otherCandidateLocations" in self.segmentdict:
            self.initOCLs()
        if "simplifiedRawPath" in self.segmentdict:
            self.initSimplifiedRawPath()
    def initLocation(self):
        self.convertLatLng(self.segmentdict["location"])
    def initCenter(self):
        self.convertLatLng(self.segmentdict)
    def initOCLs(self):
        for location in self.segmentdict["otherCandidateLocations"]:
            self.convertLatLng(location)
    
    #override
    def convertLatLng(self, latlngset):
        latlnglist = ['latitudeE7', 'longitudeE7', 'latE7', 'lngE7', 'centerLatE7', 'centerLngE7']
        super().convertLatLng(latlngset, latlnglist)

class GLHinit:
    # debug| 0:no infomation, 1: only output, 2: input and output
    debug = 0
    def __init__(self, dictionary, debug = 0):
        GLHinit.debug = debug
        self.dict = dictionary
        if GLHinit.debug  > 1 :
            print(self.dict)
            print("-----")
        
    def glhinit(self):
        i = 0
        for segment in self.dict["timelineObjects"] :
            #print(segment)
            if "activitySegment" in segment :
                # print("act")
                actseg = ActivitySegment(segment['activitySegment'])
                actseg.initActivitySegment()
                i += 1
            elif "placeVisit" in segment :
                # print("pv")
                pvseg =  PlaceVisit(segment["placeVisit"])
                pvseg.initPlaceVisit()
                i += 1
            else:
                print("undefined segment")
        print("Loaded " + str(i) + " points")
        if GLHinit.debug > 0 :
            print("-----")
            print(self.dict)
        