from brres.lib.node import Node


class Bone(Node):
    """ Bone class """

    def begin(self):
        self.index = 0
        self.bone_id = 0
        self.flags = 0
        self.billboard = 0
        self.scale = (1, 1, 1)
        self.rotation = (0, 0, 0)
        self.translation = (0, 0, 0)
        self.minimum = (0, 0, 0)
        self.maximum = (0, 0, 0)
        self.b_parent = self.child = self.next = self.prev = None


    def unpack(self, binfile):
        self.offset = binfile.start()
        binfile.readLen()
        binfile.advance(8)
        self.index, self.bone_id, self.flags, self.billboard = binfile.read('4I', 20)
        self.scale = binfile.read('3f', 12)
        self.rotation = binfile.read('3f', 12)
        self.translation = binfile.read('3f', 12)
        self.minimum = binfile.read('3f', 12)
        self.maximum = binfile.read('3f', 12)
        self.b_parent, self.child, self.next, self.prev, self.part2 = binfile.read('5i', 20)
        self.transform_matrix = binfile.read('12f', 48)
        self.inverse_matrix = binfile.read('12f', 48)
        binfile.end()

    @staticmethod
    def find_bone_at(offset, bones):
        if offset:
            for x in bones:
                if x.offset == offset:
                    return x

    @staticmethod
    def post_unpack(bones):
        for b in bones:
            b.b_parent = Bone.find_bone_at(b.b_parent, bones)
            b.child = Bone.find_bone_at(b.child, bones)
            b.next = Bone.find_bone_at(b.next, bones)
            b.prev = Bone.find_bone_at(b.prev, bones)


    def pack(self, binfile):
        self.offset = binfile.start()
        # take care of marked references
        if self.prev:
            binfile.createRefFrom(self.prev.offset, 1)
        elif self.b_parent:     # first child
            binfile.createRefFrom(self.b_parent.offset, 0, False)
        binfile.markLen()
        binfile.write('i', binfile.getOuterOffset())
        binfile.storeNameRef(self.name)
        binfile.write('5I', self.index, self.bone_id, self.flags, self.billboard, 0)
        binfile.write('3f', *self.scale)
        binfile.write('3f', *self.rotation)
        binfile.write('3f', *self.translation)
        binfile.write('3f', *self.minimum)
        binfile.write('3f', *self.maximum)
        binfile.write('i', self.b_parent.offset - self.offset) if self.b_parent else binfile.advance(4)
        binfile.mark(2)     # mark child and next
        binfile.write('i', self.prev.offset - self.offset) if self.prev else binfile.advance(4)
        binfile.write('i', self.part2)
        binfile.write('12f', *self.transform_matrix)
        binfile.write('12f', *self.inverse_matrix)
        binfile.end()


class BoneTable:
    """ Bonetable class """
    def __init__(self, binfile=None):
        if binfile:
            self.unpack(binfile)
        else:
            self.entries = []

    def unpack(self, binfile):
        """ unpacks bonetable """
        [length] = binfile.read("I", 4)
        self.entries = binfile.read("{}I".format(length), length * 4)

    def pack(self, binfile):
        length = len(self.entries)
        binfile.write("I", length)
        binfile.write("{}I".format(length), *self.entries)
