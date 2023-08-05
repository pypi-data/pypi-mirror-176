class TransformPoly:
    def __init__(self, point, angle=0):
        # Make so points are relavant to other points

        # We do this because the currentObj is not updated yet. This wont do a diff here but its good practise (look at hitboxPoly)
        self.inpPoint = point
        self.inpAngle = angle

    def start(self):
        self.points = self.inpPoint
        self.angle = self.inpAngle

    def update(self):
        pass
