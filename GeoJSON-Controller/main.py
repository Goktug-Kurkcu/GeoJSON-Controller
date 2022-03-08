import json


# -- SUCCESS --
class JSON_Process:

    def __init__(self, filePath, tableName, format = ""):
        self.filePath = filePath
        self.tableName = tableName
        self.format = format

    def openJSON(self):
        with open(f"{self.filePath}{self.tableName}.geojson") as openFile:
            file = json.load(openFile)

        return file

    def writeJSON(self):
        with open(f'{self.filePath}{self.tableName}.geojson', 'w') as createFile:
            json.dump(self.format, createFile)



# -- SUCCESS --
class TableProcess:

    # This class take table properties for create geojson file.
    # If you convert it(geojson) to shape file, you can inspect this properties.
    # In a shape;
    #   + File Path                 : filePath    => string
    #   + Shape Name                : tableName   => string
    #   + Shape Table Name          : tableName   => string
    #   + Nums of Columns in Shape  : numColumns  => integer
    #   + Them(Columns) Name        : columnsName => dictionary

    
    # __init__ ++ Redesign
    def __init__(self):
        pass

    
    # Save file this path, if filePath = "" or "./", it save same place with main.py
    def filePath(self):
        filePath = input("File Path(Path Endswith must be: '/'): ")
        return filePath

    
    # {tableName}.shp => tableName is your shapefile's name
    def tableName(self):
        tableName = input("Table Name: ")
        return tableName

    
    # Fields in .shp file
    def tableColumns(self):
        numColumns = int(input("How Many Columns Do You Create: "))
        columnsName = {}

        i = 0
        while i < numColumns:
            columnName =  input("Column Name: ")
            columnValue = input("Column Value: ")
            columnsName[columnName] = columnValue
            i += 1
        
        return columnsName



# -- SUCCESS --
class GeoJSON_Creater(TableProcess):

    #This Class is a geojson file creator.
    #You can create Polygon, Line and Point files. If you want, you can convert them to .shp file with a GIS Software.
    
    def __init__(self):
        self.filePath = TableProcess().filePath()
        self.tableName = TableProcess().tableName()
        self.tableColumn = TableProcess().tableColumns()


    # Create geojson file for polygons
    def Create_Polygon(self):

        # <POLYGON.GEOJSON> Structure
        polygon = {
            "type" : "FeatureCollection",
            "name" : self.tableName,
            "crs" :
            {
                "type" : "name",
                "properties" :
                {
                    "name" : "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features" :
            [
                {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "MultiPolygon",
                        "coordinates" :
                        [
                            [
                                [
                                    #User Will Add Coordinates
                                ]
                            ]
                        ]
                    }
                }
            ]
        }

        # Create GEOJSON File
        JSON_Process(self.filePath, self.tableName, polygon).writeJSON()


    # Create geojson file for lines
    def Create_Line(self):
        
        # <LINE.GEOJSON> Structure
        line = {
            "type" : "FeatureCollection",
            "name" : self.tableName,
            "crs" :
            {
                "type" : "name", 
                "properties" : 
                { 
                    "name" : "urn:ogc:def:crs:OGC:1.3:CRS84" 
                } 
            },
            "features" :
            [
                {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "MultiLineString",
                        "coordinates" :
                        [

                        ]
                    }
                }
            ]
        }

        # Create GEOJSON File
        JSON_Process(self.filePath, self.tableName, line)


    # Create geojson file for points
    def Create_Point(self):
        
        # <POINT.GEOJSON> Structure
        point = {
            "type" : "FeatureCollection", 
            "name" : self.tableName,
            "crs" : 
            { 
                "type" : "name", 
                "properties" : 
                { 
                    "name" : "urn:ogc:def:crs:OGC:1.3:CRS84" 
                } 
            },
            "features" :
            [
                {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "Point",
                        #"coordinates" : []  => User will add coordinate dict
                    }
                }
            ]
        }

        # Create GEOJSON File
        JSON_Process(self.filePath, self.tableName, point)



# -- SUCCESS --
class GeoJSON_Add_newFeature(TableProcess):

    def __init__(self):
        self.filePath = TableProcess().filePath()
        self.tableName = TableProcess().tableName()
        self.tableColumn = TableProcess().tableColumns()


    def User_addCoordinate(self):
        global coordinates
        coordinates = []
        numCoord = int(input("Nums of Coordinates: "))

        x = 0
        while x < numCoord:
            resetList = [] # This list will reset allways
            coordX = float(input("Coordinate(Type: Float) Latitude: ")) # Input Latitude
            coordY = float(input("Coordinate(Type: Float) Longtitude: ")) # Input Longtitude
            resetList.append(coordX)
            resetList.append(coordY)
            coordinates.append(resetList) # Add resetList to Coord list (for Create this list struct: [[X,Y], [Z,H], [Q,W]])
            x += 1
        
        return coordinates


    def Add_newPolygon(self):

        # Find and open <polygon.geojson> file
        polygon = JSON_Process(self.filePath, self.tableName).openJSON()

        # New Polygon will add this list
        featureList = polygon["features"]

        #Polygon Structure
        newPolygon = {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "MultiPolygon",
                        "coordinates" :
                        [
                            [
                                [
                                    GeoJSON_Add_newFeature().User_addCoordinate()
                                ]
                            ]
                        ]
                    }
                }

        featureList.append(newPolygon)

        JSON_Process(self.filePath, self.tableName, polygon)


    def Add_newLine(self):

        # Find and open <line.geojson> file
        line = JSON_Process(self.filePath, self.tableName).openJSON()

        # New Polygon will add this list
        featureList = line["features"]

        #Polygon Structure
        newLine = {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "MultiPolygon",
                        "coordinates" :
                        [
                                    GeoJSON_Add_newFeature().User_addCoordinate()
                        ]
                    }
                }

        featureList.append(newLine)

        JSON_Process(self.filePath, self.tableName, line)


    def Add_newPoint(self):

        # Find and open <point.geojson> file
        point = JSON_Process(self.filePath, self.tableName).openJSON()

        # New Polygon will add this list
        featureList = point["features"]
        #Polygon Structure
        newPoint = {
                    "type" : "Feature",
                    "properties" : self.tableColumn,
                    "geometry" :
                    {
                        "type" : "MultiPolygon",
                        "coordinates" : GeoJSON_Add_newFeature().User_addCoordinate()[0]
                    }
                }
                
        featureList.append(newPoint)

        JSON_Process(self.filePath, self.tableName, point).openJSON()



# -- SUCCESS --
class GeoJSON_Coordinate_Change(TableProcess):

    # This class is Controller. You can add coordinates in your geojson files.
    # The version 1.0 is only support .txt files.
    # Your <COORD.txt> must have this structure for your coordinates:
    # [12.1234, 45.6789],
    # [67.8901, 89.0123]
    # or
    # [12.1234,45.6789], [67.8901, 89.0123]

    def __init__(self):
        self.filePath = TableProcess().filePath()
        self.tableName = TableProcess().tableName()


    def findCoordFile(self):
        # This function mission is : User add path, Func find file and read coordinates.
        # And return them. 
        coordPath = input("Coord File Path(Support only .txt files.): ")

        with open(coordPath, "r") as findCoord:
            coords = findCoord.read() 

        return coords


    def Update_PolyCoords(self):
        
        # Find and open <polygon.geojson> file
        polygon = JSON_Process(self.filePath, self.tableName).openJSON()

        #Coordinate List in <Polygon.GeoJSON> Structure
        coordList = polygon["features"][0]["geometry"]["coordinates"][0][0]

        # Change coordinates
        coordinates = GeoJSON_Coordinate_Change().findCoordFile() # => coordinates return => "[[x,y], [z,p], ...]"
        coordinates = json.loads(coordinates) # => coordinates turned; => [[x,y], [z,p]]
        coordList.append(coordinates) 

        JSON_Process(self.filePath, self.tableName, polygon).writeJSON()


    def Update_LineCoords(self):
        # Find and open <line.geojson> file
        line = JSON_Process(self.filePath, self.tableName).openJSON()
        
        #Coordinate List in <Line.GeoJSON> Structure
        coordList = line["features"][0]["geometry"]["coordinates"]

        # Change coordinates
        coordinates = GeoJSON_Coordinate_Change().findCoordFile() # => coordinates return => "[[x,y], [z,p], ...]"
        coordinates = json.loads(coordinates) # => coordinates turned; => [[x,y], [z,p]]
        coordList.append(coordinates)

        JSON_Process(self.filePath, self.tableName, line).writeJSON()


    def Update_PointCoords(self):
        # Find and open <point.geojson> file
        point = JSON_Process(self.filePath, self.tableName).openJSON()
        
        #Coordinate List in <Point.GeoJSON> Structure
        coordList = point["features"][0]["geometry"]

        # Change coordinates
        coordinates = GeoJSON_Coordinate_Change().findCoordFile() # => coordinates return => "[x,y]"
        coordinates = json.loads(coordinates) # => coordinates turned; => [x,y]
        coordList["coordinates"] = coordinates

        JSON_Process(self.filePath, self.tableName, point).writeJSON()



# -- SUCCESS --
class GeoJSON_Property_Change(TableProcess):
    
    def __init__(self):
        self.filePath = TableProcess().filePath()
        self.tableName = TableProcess().tableName()
    

    # Take input from user for change <*>.geojson file properties
    def UserInput_forChange(self):
        global changeKey
        changeKey = input("Column Name: ")
        global changeValue 
        changeValue = input("Value: ")


    # Change Polygon Attribute
    def Polygon_Attribute(self):

        # Find and open <polygon.geojson> file
        polygon = JSON_Process(self.filePath, self.tableName).openJSON()

        # Use Function for take user inputs
        GeoJSON_Property_Change().UserInput_forChange()
        
        #Properties Dictionary in <Polygon.GeoJSON> Structure
        properties = polygon["features"][0]["properties"]
        properties[changeKey] = changeValue
        
        # Save File
        JSON_Process(self.filePath, self.tableName, polygon).writeJSON()


    # Change Line Attribute
    def Line_Attribute(self):

        # Find and open <line.geojson> file
        line = JSON_Process(self.filePath, self.tableName).openJSON()

        # Use Function for take user inputs
        GeoJSON_Property_Change().UserInput_forChange()
        
        #Properties Dictionary in <Line.GeoJSON> Structure
        properties = line["features"][0]["properties"]
        properties[changeKey] = changeValue
        
        # Save File
        JSON_Process(self.filePath, self.tableName, line).writeJSON()


    # Change Point Attribute
    def Point_Attribute(self):

        # Find and open <point.geojson> file
        point = JSON_Process(self.filePath, self.tableName).openJSON()

        # Use Function for take user inputs
        GeoJSON_Property_Change().UserInput_forChange()
        
        #Properties Dictionary in <Point.GeoJSON> Structure
        properties = point["features"][0]["properties"]
        properties[changeKey] = changeValue
        
        # Save File
        JSON_Process(self.filePath, self.tableName, point).writeJSON()


#---SUCCESS---
# GeoJSON_Creater().Create_Polygon()
# input("Polygon was Created.")
# GeoJSON_Creater().Create_Line()
# input("Line was Created.")
# GeoJSON_Creater().Create_Point()
# input("Point was Created.")
#-------------------------------------
# GeoJSON_Coordinate_Change().Update_PolyCoords()
# input("Coordinates was Changed.")
# GeoJSON_Coordinate_Change().Update_LineCoords()
# input("Coordinates was Changed.")
# GeoJSON_Coordinate_Change().Update_PointCoords()
# input("Coordinates was Changed.")
#-------------------------------------
# GeoJSON_Property_Change().Polygon_Attribute()
# input("Properties was Changed".)
# GeoJSON_Property_Change().Line_Attribute()
# input("Properties was Changed.")
# GeoJSON_Property_Change().Point_Attribute()
# input("Properties was Changed.")
#-------------------------------------
# GeoJSON_Add_newFeature().Add_newPolygon()
# input("Feature was Added.")


#---'ll Try---
# GeoJSON_Add_newFeature().Add_newLine()
# input("Feature was Added.")
# GeoJSON_Add_newFeature().Add_newPoint()
# input("Feature was Added.")
