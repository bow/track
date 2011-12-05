"""
This subpackage contains one python source file per format implemented for serialization.
"""

# Built-in modules #
import sys

# Other modules #
import bbcflib.genrep
genrep = bbcflib.genrep.GenRep()

# Variables #
serializers = {
    'memory':   {'module': 'track.serialize.memory',   'class': 'SerializerRAM'},
    'sql':      {'module': 'track.serialize.sql',      'class': 'SerializerSQL'},
    'bed':      {'module': 'track.serialize.bed',      'class': 'SerializerBED'},
    'wig':      {'module': 'track.serialize.wig',      'class': 'SerializerWIG'},
    'gff':      {'module': 'track.serialize.gff',      'class': 'SerializerGFF'},
    'gtf':      {'module': 'track.serialize.gtf',      'class': 'SerializerGTF'},
    'bedGraph': {'module': 'track.serialize.bedGraph', 'class': 'SerializerBedGraph'},
    'bigWig':   {'module': 'track.serialize.bigWig',   'class': 'SerializerBigWig'},
}

################################################################################
def get_serializer(path, format):
    """Given a path and a format will return the appropriate serializer.

            * *path* is a string specifying the path of the track to parse.
            * *format* is a string specifying the format of the track to parse.

        Examples::

            import track.parse
            import track.serialze
            serializer = track.serialize.get_serializer('tmp/test.sql', 'sql')
            parser = track.parse.get_parser('tmp/test.bed', 'bed')
            parser(serializer)

        ``get_serializer`` returns a Serializer instance.
    """
    if not format in serializers: raise Exception("The format '%s' is not supported." % format)
    info = serializers[format]
    # Import the objects #
    base_module    = __import__(info['module'])
    sub_module     = sys.modules[info['module']]
    class_object   = getattr(sub_module, info['class'])
    class_instance = class_object(path)
    # Return an instance #
    return class_instance

################################################################################
class Serializer(object):
    def __init__(self, path):
        self.path = path
        self.tracks = []

    def __enter__(self):
        return self

    def __exit__(self, errtype, value, traceback):
        pass

    def error(self, message, path=None, line_number=None):
        if path:
            if not line_number: location = " '" + path + "'"
            else: location = " '" + path + ":" + str(line_number) + "'"
            raise Exception(message % location)
        raise Exception(message)

    def defineFields(self, fields):
        pass

    def defineChrmeta(self, chrmeta):
        self.chrmeta = chrmeta

    def defineAssembly(self, assembly):
        self.defineChrmeta(genrep.get_chrmeta(genrep.assembly(assembly).name))

    def newTrack(self, info=None, name=None):
        pass

    def newFeature(self, chrom, feature):
        raise NotImplementedError

#-----------------------------------#
# This code was written by the BBCF #
# http://bbcf.epfl.ch/              #
# webmaster.bbcf@epfl.ch            #
#-----------------------------------#
