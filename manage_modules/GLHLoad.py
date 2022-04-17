# GLHLoad.py

class GLHInitialize:
    def __init__(self, dictionary):
        self.dict = dictionary
        
    def initialize(self):
        loaded_segments_num = 0
        for segment in self.dict["timelineObjects"] :
            #print(segment)
            status = self._segment_initialize(segment)
            loaded_segments_num += 1 if status else 0
    
        print("Loaded " + str(loaded_segments_num) + " points")
    
    def _segment_initialize(self, segment):
        if "activitySegment" in segment :
            # print("act")
            actseg = ActivitySegment(segment['activitySegment'])
            actseg.initialize()
            return True
        elif "placeVisit" in segment :
            # print("pv")
            pvseg =  PlaceVisit(segment["placeVisit"])
            pvseg.initialize()
            return True
        else:
            print("undefined segment")

        return False

# activitysegmentとplacevisitの親クラス
class ParentGLHSegment:
    def __init__(self, segmentdata):
        self.segmentdict = segmentdata
    
    def offset_lat_lng (self, coordinate, latlnglist = ['latitudeE7', 'longitudeE7', 'latE7', 'lngE7']):
        offset = 10000000
        for i in latlnglist:
            if i in coordinate :
                coordinate[i] = coordinate[i] / offset
            else:
                pass
        
    def cast_timestamp (self, timestamp):
        return int(timestamp)
        
    def _init_duration (self):
        duration = self.segmentdict['duration']
        for k,v in duration.items():
            duration[k] = self.cast_timestamp(v)

    def _init_simplified_raw_path(self):
        simplifiedRawPath = self.segmentdict['simplifiedRawPath']
        for point in simplifiedRawPath['points']:
            self.offset_lat_lng(point)
            point['timestampMs'] = self.cast_timestamp(point['timestampMs'])

    def print (self):
        print(self.segmentdict)

class ActivitySegment(ParentGLHSegment):
    def __init__(self, segmentdata):
        super().__init__(segmentdata)
    
    def initialize(self):
        self._init_location()
        self._init_duration()
        if "waypointPath" in self.segmentdict:
            self._init_waypoint_path()
        if "simplifiedRawPath" in self.segmentdict:
            self._init_simplified_raw_path()

    def _init_location(self):
        self.offset_lat_lng(self.segmentdict['startLocation'])
        self.offset_lat_lng(self.segmentdict['endLocation'])

    def _init_waypoint_path(self):
        waypoint_path = self.segmentdict['waypointPath']
        for i in waypoint_path['waypoints']:
            self.offset_lat_lng(i)
    
class PlaceVisit(ParentGLHSegment):
    def __init__(self, segmentdata):
        super().__init__(segmentdata)

    def initialize(self):
        self._init_location()
        self._init_duration()
        self._init_center()
        if "otherCandidateLocations" in self.segmentdict:
            self._init_other_candidate_locations()
        if "simplifiedRawPath" in self.segmentdict:
            self._init_simplified_raw_path()

    def _init_location(self):
        self.offset_lat_lng(self.segmentdict["location"])

    def _init_center(self):
        self.offset_lat_lng(self.segmentdict)

    def _init_other_candidate_locations(self):
        for location in self.segmentdict["otherCandidateLocations"]:
            self.offset_lat_lng(location)
    
    #override
    def offset_lat_lng(self, latlngset):
        latlnglist = ['latitudeE7', 'longitudeE7', 'latE7', 'lngE7', 'centerLatE7', 'centerLngE7']
        super().offset_lat_lng(latlngset, latlnglist)


        