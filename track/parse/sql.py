"""
This module implements the parsing of the track object.
In this case the self.path attribute can be either
a Track object or the path to an SQL file.
"""

# Internal modules #
from track import Track, load
from track.parse import Parser

################################################################################
class ParserSQL(Parser):
    def parse(self):
        # Core function #
        def read_whole_track(t):
            self.handler.defineFields(t.fields)
            self.handler.newTrack(t.info)
            for chrom in t:
                for feature in t.read(chrom):
                    self.handler.newFeature(chrom, feature)
        # Check param type #
        if isinstance(self.path, Track):
            read_whole_track(self.path)
        else:
            with load(self.path, 'sql') as t: read_whole_track(t)

#-----------------------------------#
# This code was written by the BBCF #
# http://bbcf.epfl.ch/              #
# webmaster.bbcf@epfl.ch            #
#-----------------------------------#
