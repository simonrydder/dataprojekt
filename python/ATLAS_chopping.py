def findingIndex(A, D):
    zA, yA, xA = A.shape
    zD, yD, xD = D.shape

    for z in range(zA - zD):
        for y in range(yA - yD):
            for x in range(xA - xD):
                if (A[z : z + zD, y : y + yD, x : x + xD] == D).all():
                    return (z, y, x)
    
    return (0, 0, 0)

if __name__ == '__main__':
    from DataPreparation import OAR_Image
    from DataReader import Path

    segment = 'brain'
    ID = '4Prj3A5sMvSv1sK4u5ihkzlnU'
    Date = '20190129'
    PA = Path(ID, Date, 'AGT')
    PD = Path(ID, Date, 'GT')

    A = OAR_Image(PA, segment).GetArray()
    D = OAR_Image(PD, segment).GetArray()
    print(A.shape)
    print(D.shape)
    print(findingIndex(A, D))