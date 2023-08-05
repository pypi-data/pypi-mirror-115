# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:48:31 2021

@author: jon-f
"""

import os
import subprocess
import threading
from datetime import date
import glob
import time
import math
from IPython.display import display
import datetime as dt
import pytz
import matplotlib.pyplot as plt
import urllib
import numpy as np
import folium
import ee
from google.cloud import storage

def auth():
    """
    Authenticates the user to Google Earth Engine and initializes the library.

    Args:
        None.

    Returns:
        client (storage.Client): A Client object that can be used to access \
            Google Cloud Storage data.

    """
    while True:
        try:
            service_account = input("Enter your service account email: ")
            json_file = ''
            for file in os.listdir():
                if file.endswith('.json'):
                    json_file = file
                    break
            credentials = ee.ServiceAccountCredentials(service_account, json_file)
            ee.Initialize(credentials=credentials)
            client_obj = storage.Client(credentials=credentials)        
            break
        except KeyboardInterrupt:
            break
        
        except:
            print("The JSON private key file could not be found or was inconsistent \
    with the service account. Please only one key in the current file directory.")
    
    return client_obj

client = auth()

# reducer
def divider(coordinates):

    assert np.array(coordinates).shape[1] == 2, "Coordinates of wrong size [error]"
    def checkifrect(nparray):
        pone, ptwo, pthree, pfour, pfive = nparray
        v1_mag = np.linalg.norm(np.subtract(pthree, pone))
        v2_mag = np.linalg.norm(np.subtract(pfour, ptwo))
        return bool(np.abs(v1_mag-v2_mag) < 0.001)

    assert checkifrect(coordinates), "The input geometry must be rectangular"

    x_data = coordinates[:, 0]
    y_data = coordinates[:, 1]

    (c_x, c_y) = (np.sum(x_data[:-1])/np.size(x_data[:-1]),
                  np.sum(y_data[:-1])/np.size(y_data[:-1]))
    new_polygons = []
    corners = len(coordinates)-1

    for i in range(corners):
        polygon = [[x_data[i], y_data[i]],
                   [(x_data[i%corners]+x_data[(i+1)%corners])/2,
                    (y_data[i%corners]+y_data[(i+1)%corners])/2],
                   [c_x, c_y],
                   [(x_data[i]+x_data[(i-1)%corners])/2,
                    (y_data[i]+y_data[(i-1)%corners])/2],
                   [x_data[i], y_data[i]]]
        new_polygons.append(polygon)
    return new_polygons

def rect_area(coordinates):
    try:
        np.array(coordinates).shape[1] == 2
        p1, p2, p3, p4, p5 = coordinates
    except:
        coordinates = primer(coordinates)[0]
        p1, p2, p3, p4, p5 = coordinates

    area = np.abs(np.linalg.norm(p2-p1)*np.linalg.norm(p4-p1))
    return area

def all_good(listOfCoords):
    flag = True
    for coords in listOfCoords:
        if rect_area(coords) > 0.1: # arbitary value
            flag = False
            break
    return flag

def primer(area):
        l1 = [area,]
        l2 = np.array(l1)
        l3 = np.reshape(l2,(l2.shape[0], l2.shape[2], 2))
        return l3

def reduce(listOfCoords):
    """
    Divides a rectangles defined by closed coordinates into smaller, rectangles.

    Args:
        listOfCoords (list): A list of coordinates in the form \
            [[[x1, y1], [x2, y2], ...., [x1, y1]], ...]. The \
            coordinates must define a rectangular shape.
    Returns:
        new_polygons (list): A set of new rectangular in the form \
            [coordinates1, coordinates2, ..., coordinatesn] where n is \
            the number number of length of coordinates-1 (the number of corners)

    """
    try:
        listOfCoords[1]
    except:
        listOfCoords = primer(listOfCoords)
    assert listOfCoords.shape[2] == 2, "wrong size error"

    if all_good(listOfCoords):
        return listOfCoords

    newlistOfCoords = []
    for coords in listOfCoords:
        newlistOfCoords = newlistOfCoords + divider(coords)

    newlistOfCoords = np.squeeze(np.array(newlistOfCoords))
    return reduce(listOfCoords=newlistOfCoords)


def geoJSONer(coords):
    try:
        coords = coords.tolist()
    except:
        pass
    
    geoJSON = {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Polygon",
              "coordinates": [
                coords
              ]
            }
          }
        ]
    }

    return geoJSON

def degeoJSONer(geoJSON):
    coords = geoJSON['features'][0]['geometry']['coordinates']
    return coords

# gammamap
def gammamap(image):

    """
    Gamma Maximum a-posterior Filter applied to one image. It is implemented as \
        described in Lopes A., Nezry, E., Touzi, R., and Laur, H., 1990. \
        Maximum A Posteriori Speckle Filtering and First Order texture Models \
        in SAR Images. International  Geoscience  and  Remote  Sensing  Symposium.

    Parameters
    ----------
    image : ee.Image
        Image to be filtered
    Returns
    -------
    ee.Image
        Filtered Image
    """
    enl = 5
    KERNEL_SIZE=3
    try:
        bandNames = image.bandNames().remove('angle')
    except:
        bandNames= image.bandNames()
    #local mean
    reducers = ee.Reducer.mean().combine( \
                      reducer2= ee.Reducer.stdDev(), \
                      sharedInputs= True
                      )
    stats = (image.select(bandNames).reduceNeighborhood( \
                      reducer= reducers, \
                          kernel= ee.Kernel.square(KERNEL_SIZE/2,'pixels'), \
                              optimization= 'window'))
    meanBand = bandNames.map(lambda bandName: ee.String(bandName).cat('_mean'))
    stdDevBand = bandNames.map(lambda bandName:  ee.String(bandName).cat('_stdDev'))

    z = stats.select(meanBand)
    sigz = stats.select(stdDevBand)

    #local observed coefficient of variation
    ci = sigz.divide(z)
    #noise coefficient of variation (or noise sigma)
    cu = 1.0/math.sqrt(enl)
    #threshold for the observed coefficient of variation
    cmax = math.sqrt(2.0) * cu
    cu = ee.Image.constant(cu)
    cmax = ee.Image.constant(cmax)
    enlImg = ee.Image.constant(enl)
    oneImg = ee.Image.constant(1)
    twoImg = ee.Image.constant(2)

    alpha = oneImg.add(cu.pow(2)).divide(ci.pow(2).subtract(cu.pow(2)))

    #Implements the Gamma MAP filter described in equation 11 in Lopez et al. 1990
    q = image.select(bandNames).expression(
        'z**2 * (z * alpha - enl - 1)**2 + 4 * alpha * enl * b() * z',
        { 'z': z,  'alpha':alpha,'enl': enl})
    rHat = z.multiply(alpha.subtract(enlImg).subtract(oneImg))\
        .add(q.sqrt()).divide(twoImg.multiply(alpha))

    #if ci <= cu then its a homogenous region ->> boxcar filter
    zHat = (z.updateMask(ci.lte(cu))).rename(bandNames)
    #if cmax > ci > cu then its a textured medium ->> apply Gamma MAP filter
    rHat = (rHat.updateMask(ci.gt(cu)).updateMask(ci.lt(cmax))).rename(bandNames)
    #ci>cmax then its strong signal ->> retain
    x = image.select(bandNames).updateMask(ci.gte(cmax)).rename(bandNames)
    #Merge
    output = ee.ImageCollection([zHat,rHat,x]).sum()
    redone = image.addBands(output, None, True)
    final = redone.toFloat()
    return final

# downlaod functions
def DLimg(image, directory, scale, aoi):
    """
    Downloads an image or image collection.

    Args:
        images (ee.Image or ee.ImageCollection): images to download
        directory (str): name of relative directory to save images to, \
            leave as a blank string you'd like to save in current directory

    Returns:
        None.
    """

    imageID = image.id().getInfo()
    def nextfile(imageID):
        def filenamer(imageID, i):
            name = imageID + '_' + str(i) + ".tif"
            filename = os.path.join(os.getcwd(), directory, name)
            return filename

        i = 0
        while os.path.isfile(filenamer(imageID, i)):
            i += 1
        return filenamer(imageID, i)

    url = image.clip(aoi).getThumbURL({'format': 'geotiff', 'scale': scale})

    filepath = nextfile(imageID)
    urllib.request.urlretrieve(url, filepath)
    print(url, "has been downloaded to", str(filepath))

def merger(directory='export'):
    """
    Run this function after the download is complete to have gdal attempt \
        to merge the geoTIFFs. Generally should not used on it's own.

    Args:
        directory (str): The directory to find the unmerged TIF images in. Defaults to 'export'

    Returns:
        None.

    """
    tiles = glob.glob((directory+'/*.tif'))
    tiles = " ".join(tiles)

    name = directory + "/" + tiles[tiles.find('/')+1:tiles.find('.tif')-2] + ".tif"
    print(name)

    os.system('!gdal_merge.py -o $name $tiles')

    if os.path.isfile(name):
        for file in os.scandir(directory):
            if file.path.endswith('.tif') and file.path.count('_')==9:
                print(file.path, 'has been deleted!')
                os.remove(file.path)
    else:
        assert True, "gdal_merge was not found, \
try restarting the kernel and running merger(directory)"

def batchExport(images, scale, coords, cloud_bucket='', directory='', tryReduce=False):
    """
    Creates a number of ee.batch tasks equal to the number of ee.Image objects in images. \
        The images are downloaded to the Google Cloud Platform Storage glaciers_ee \
        bin in the subdirectory set.

    Args:
        images (list): a list of images to export to cloudstorage
        scale (int): the scale in meters/pixel to download the images at
        directory (str): the subdirectory to download the images to in the \
            glaciers_ee bin. Defaults to 'export'

    Returns:
        None.
    """
    images_sort = images[:]
    def start_tasks(images, scale, cloud_bucket, directory):
        for img in images:
            name = img.get('system:index').getInfo()
            try: 
                name + ''
            except:
                name = img.get('system:id').getInfo().replace("/", "")
            task = ee.batch.Export.image.toCloudStorage(**{
                'image': img,
                'fileNamePrefix': directory + '/' + name,
                'region': ee.Geometry.Polygon(coords),
                'scale': scale,
                'crs': 'EPSG:3031',
                'bucket': cloud_bucket,
                'fileFormat': 'GeoTIFF',
                'maxPixels': 10e12
            })
            print(name, "is being uploaded.")
            task.start()
            tasks.append(task)
            active_ind.append(task.active())

    def time_for_completion(active_ind, scale, rate=1.5):
        num_imgs = active_ind.count(True)
        try:
            time_left = (num_imgs * rect_area(coords)/scale * 1/rate * 3600)**(3/4) # hours
        except:
            time_left = 0
            
        if time_left < 1/60:
            time_left *= 3600
            units = 'seconds'
        elif time_left < 1.0:
            time_left *= 60
            units = 'minutes'
        else:
            units = 'hours'

        completion_string = 'The approximate completion time is: {:.1f} {}.'\
        .format(time_left, units)
        return completion_string

    def reduced_upload(failed_task, scale, cloud_bucket, directory):
        failed_i = tasks.index(failed_task)
        failed_image = images_sort[failed_i]
        image_coordinates = failed_image.get('system:foodprint').getInfo()['coordinates']
        image_segmented = reduce(image_coordinates)
        n = 0
        for coords in image_segmented.tolist():
            name = failed_image.get('system:index').getInfo()
            name_n = name + '_' + str(n)
            new_aoi = ee.Geometry.Polygon([coords])
            task = ee.batch.Export.image.toCloudStorage(**{
                'image': failed_image,
                'region': new_aoi,
                'fileNamePrefix': directory + '/' + name_n,
                'scale': scale,
                'crs': 'EPSG:3031',
                'bucket': cloud_bucket,
                'fileFormat': 'GeoTIFF',
                'maxPixels': 10e12
            })
            task.start()
            tasks.append(task)
            active_ind.append(task.active())
            images_sort.append(failed_image.clip(new_aoi))
            n += 1

        tasks.pop(failed_i)
        active_ind.pop(failed_i)
        images_sort.pop(failed_i)


    def status_check(tasks):            
        tasks_copy = tasks[:]
        
        for task in tasks_copy:
            if task.status()['state'].lower() == "failed" and tryReduce:
                print('Task #{} has failed.'.format(task.id),
                      'Trying geometrically reduced uploads.')
                reduced_upload(task, scale, cloud_bucket, directory)
            elif task.status()['state'].lower() == "failed":
                active_ind[tasks.index(task)] = False
                print('The upload has failed, most likely due to the GEE', 
                      '10e12 pixel limitation. Try a smaller sized geoJSON or tryReduce.',
                      'The cloud_bucket set should also be checked to see it exists.')
            elif task.status()['state'].lower() == "completed":
                active_ind[tasks.index(task)] = False
            else:
                print('{} is {}'.format('Task #' + task.id,
                                        task.status()['state'].lower()))
                
    tasks = []
    active_ind = []
    STARTED_TASKS = False
    start_time = dt.datetime.now(pytz.utc)

    while True:
        try:
            if not STARTED_TASKS:
                start_tasks(images, scale, cloud_bucket, directory)
                STARTED_TASKS = True
    
            print(time_for_completion(active_ind, scale))
            
            print('----------------------------------------------------')
            time.sleep(5*active_ind.count(True)**(1/2))
            
            status_check(tasks)
                
            if True not in active_ind:
                break
        except KeyboardInterrupt:
            for task in tasks:
                task.cancel()
            break
        
    def get_new(start_time):
        bucket = client.get_bucket(cloud_bucket)
        blobs = client.list_blobs(bucket)
        new_blobs = []
        for blob in blobs:
            dateandtime = blob.updated
            if dateandtime > start_time:
                new_blobs.append(blob)
                
        return new_blobs
    
    def download_list_of_blobs(list_of_blobs):
        def nextfile(blob_name):
            def filenamer(i, blob_name):
                name = blob_name[:-4] + '_' + str(i) + ".tif"
                filename = os.path.join(os.getcwd(), name)
                return filename
            i = 0
            while os.path.isfile(filenamer(i, blob_name)):
                i += 1
            return filenamer(i, blob_name)
        
        for blob in list_of_blobs:
            filename = nextfile(blob_name=blob.name)
            try:
                with open(filename, 'w'):
                    pass
                blob.download_to_filename(filename)
                print('Downloading image as {}'.format(os.path.abspath(filename)))
            except FileNotFoundError:
                print('ERROR: Directory does not exist on disk!',
                      'Please create it first.')
            
    new = get_new(start_time)
    download_list_of_blobs(new)

def cloudtoeecommand(cloud_bucket, directory, assetname, geeusername):
    """
    Returns an ee.Image from a cloud storage asset. Requirement:
        must have a username and main folder with Google code editor
    
    Args: 
        cloud_bucket (str): string describing the name of the cloud bucket
        directory (str): directory describing the directory where the file is stored
        assetname (str): the filename of the asset (without .tif)
        geeusername (str): your username to store the asset in the code editor
        
    Returns:
        eeimage (ee.Image): the ee.Image object of the google cloud asset
    """
    
    if assetname.endswith('.tif'):
        assetname = assetname[:-4]
    
    asset_id = 'users/' + geeusername + '/' + assetname
    dl_dir = 'gs://' + cloud_bucket + '/' + directory
    dl_file = dl_dir + '/' + assetname + '.tif'
        
    command = f'earthengine upload image --asset_id={asset_id} {dl_file}'
    
    pop = subprocess.Popen(command, env=os.environ.copy(),
                            shell=True, stdout=subprocess.PIPE)
    result = pop.stdout.read().decode()
    taskid = result[result.index(':')+2:result.index('\r')]
    
    while True:
        try:
            command = f'earthengine task info {taskid}'
            pop = subprocess.Popen(command, env=os.environ.copy(),
                                shell=True, stdout=subprocess.PIPE)
            status = pop.stdout.read().decode().split(' ')[3]
            if 'COMPLETED' in status:
                break
            elif 'FAILED' in status:
                return None
                break
            print(f'Task #{taskid} is {status.lower().strip()}')
            time.sleep(8)
        except:
            command = f'earthengine task cancel {taskid}'
            pop = subprocess.Popen(command, env=os.environ.copy(),
                                shell=True, stdout=subprocess.PIPE)
        
    command = f'earthengine acl set public {asset_id}'
    pop = subprocess.Popen(command, env=os.environ.copy(),
                           shell=True, stdout=subprocess.PIPE)
    time.sleep(1)

    if assetname.startswith('S1'):    
        def extract_date(assetname):
            val = -1
            for i in range(4):
                val = assetname.find("_", val+1)
            datestr = assetname[val+1:assetname.find("_", val+1)]
            formatted_date = datestr[:4] + '-' + datestr[4:6] + '-' + datestr[6:11] \
                + ':' + datestr[11:13] + ':' + datestr[13:15]
            return formatted_date
        
        command = f'earthengine asset set --time_start {extract_date(assetname)} {asset_id}'
        pop = subprocess.Popen(command, env=os.environ.copy(),
                                shell=True, stdout=subprocess.PIPE)
    eeimage = ee.Image(asset_id)
    print(f'Task #{taskid} is available at {asset_id}')
    
    return eeimage

def multicloudtoee(cloud_bucket, directory, geeusername):
    '''
    Creates callable image assets from all the Tiffs in a Cloud Directory. \
        Requirement: must have a username and main folder with Google code editor
    
    Args: 
        cloud_bucket (str): string describing the name of the cloud bucket
        directory (str): directory describing all the images you'd like to upload
        geeusername (str): your username to store the asset in the code editor
        
    Returns:
        None
    '''
    bucket = client.get_bucket(cloud_bucket)
    blobs = client.list_blobs(bucket)
    
    threads = []
    assets = []
    
    for blob in blobs:
        
        ind = str(blob).find('/')
        find = ' ' + directory
        if str(blob)[ind-1:ind-len(find)-1:-1] != find[::-1]: 
            # if directory doesn't match, continue to next iter
            continue
        
        if str(blob)[ind:str(blob).find(',', ind)].strip() == '/':
            # if blob is the actual directory and not a file, continue
             continue
        
        blob_info = str(blob).split(' ')
        
        assetname = blob_info[2][blob_info[2].find('/')+1:-1]
        if assetname.endswith('.tif'):
            assetname = assetname[:-4]
        asset_id = 'users/' + geeusername + '/' + assetname
        assets.append(asset_id)
        def do_convert():
            cloudtoeecommand(cloud_bucket, directory, assetname, geeusername)
        
        while True:
            alive_count = 0
            for thread in threads:
                if thread.is_alive(): alive_count += 1 
            if alive_count < 10:
                break
            else:
                time.sleep(10)
                print(f'Alive count: {alive_count}')
            
        t = threading.Thread(target=do_convert)
        t.daemon = True
        threads.append(t)
        t.start()

    for i in range(len(threads)):
        threads[i].join()

    image_objs_list = [ee.Image(asset) for asset in assets]

    return image_objs_list

    '''
    Creates callable image assets from all the Tiffs in a Cloud Directory. \
        Requirement: must have a username and main folder with Google code editor
    
    Args: 
        cloud_bucket (str): string describing the name of the cloud bucket
        directory (str): directory describing all the images you'd like to upload
        geeusername (str): your username to store the asset in the code editor
        
    Returns:
        None
    '''
    bucket = client.get_bucket(cloud_bucket)
    blobs = client.list_blobs(bucket)
    
    threads = []
    
    for blob in blobs:
        
        ind = str(blob).find('/')
        find = ' ' + directory
        if str(blob)[ind-1:ind-len(find)-1:-1] != find[::-1]: 
            # if directory doesn't match, continue to next iter
            continue
        
        if str(blob)[ind:str(blob).find(',', ind)].strip() == '/':
            # if blob is the actual directory and not a file, continue
             continue
        
        blob_info = str(blob).split(' ')
        
        def do_convert():
            assetname = blob_info[2][blob_info[2].find('/')+1:-1]
            cloudtoeecommand(cloud_bucket, directory, assetname, geeusername)
        
        while True:
            alive_count = 0
            for thread in threads:
                if thread.is_alive(): alive_count += 1 
            if alive_count < 10:
                break
            else:
                time.sleep(10)
                print(f'Alive count: {alive_count}')
            
        t = threading.Thread(target=do_convert)
        t.daemon = True
        threads.append(t)
        t.start()

    for i in range(len(threads)):
        threads[i].join()

    return None
# folium maps
def add_ee_layer(self, ee_image_object, vis_params, name):
    """
    Adds an ee.Image layer to a folium map

    Args:
        ee_image_object (ee.Image): An image to place on folium map
        vis_params (dict): Visual parameters to display the image. See GEE "Image Visualization"
        name (str): Name of layer on folium map

    Returns:
        None.

    """
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles = map_id_dict['tile_fetcher'].url_format,
        attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name = name,
        overlay = True,
        control = True
    ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer


def eeICtolist(imageCollection):
    """
    Converts an ee.ImageCollection to a python list of ee.Image objects.

    Args:
        imageCollection (ee.ImageCollection): the collection to be converted to a list

    Returns:
        images (list): the list of images in the ee.ImageCollection

    """
    size = imageCollection.size()
    eeList = imageCollection.toList(size)
    aslist = []
    for i in range(size.getInfo()):
        aslist.append(ee.Image(eeList.get(i)))

    return aslist

def dispHist(hists):
    """
    Plots 1 histogram for each histogram passed into it.

    Args:
        hists (list): Can either be a histogram from Area.hist() or \
            a list of histograms [Area.hist(img1), Area.hist(img2)]

    Returns:
        None.
    """
    assert isinstance(hists, list), "Type of hists should be a list from self.hist, or a list of lists"
    a = np.array(hists)
    if a.ndim == 3:
        # case for hists is a list of histograms
        for hist in hists:
            a = np.array(hist)
            x = a[:, 0]
            y = a[:, 1]/np.sum(a[:, 1])
            plt.grid()
            plt.plot(x, y, '.')
            plt.show()
    else:
        # case for hists is single histogram
        x = a[:, 0]
        y = a[:, 1]/np.sum(a[:, 1])
        plt.grid()
        plt.plot(x, y, '.')
        plt.show()

def get_dates(images):
    """
    Returns the dates of each image in imageCllection

    Args:
        images (ee.Image or ee.ImageCollection): Image/images to get the date of

    Returns:
        dates (str or list): The dates that the images were taken on
    """
    try:
        if isinstance(images, ee.ImageCollection):
            dates = ee.List(images
                            .aggregate_array('system:time_start')
                            .map(lambda time_start:
                                 ee.Date(time_start).format('Y-MM-dd'))).getInfo()
        elif isinstance(images, ee.Image):
            dates = ee.Date(images.get('system:time_start').getInfo()).format("yyyy-MM-dd").getInfo()

        else:
            assert True, "Image is not of type ee.Image or ee.ImageCollection"
        return dates
    except:
        print('ERROR: Something went wrong and the Image does \
not have the system:time_start property.')
        print('If you need the date, you can manually retrieve \
it from the system:index property')
        return None


class Area:
    """
    This is the main class. Defined by the geoJSON inputed by the user, \
        it contains methods for displaying, operating on, and downloading
        ee.Images and ee.ImageCollections.

    Args:
        geoJSON (dict):  The geoJSON defining a singular geographical area. \
            See https://geojson.io/.

    """
    def __init__(self, geoJSON):
        self.geoJSON = geoJSON
        self.coords = self.geoJSON['features'][0]['geometry']['coordinates']
        self.aoi = ee.Geometry.Polygon(self.get_coords())

    def get_coords(self):
        """
        Gets the coordinates defined by the geoJSON.

        Args:
            None.

        Returns:
            self.coords (list): The coordinates defined by the geoJSON.

        """
        return self.coords

    def get_aoi(self):
        """
        Gets the AOI defined by the coordinates.

        Args:
            None.

        Returns:
            self.aoi (list): The AOI defined by the coordinates.

        """
        return self.aoi

    def apply_filters(self, collection='COPERNICUS/S1_GRD_FLOAT',
                      start_date=ee.Date(0),
                      end_date=ee.Date(date.today().isoformat()),
                      tRP1=None, tRP2=None, res=None, ins=None, earliest_first=False):
        """
        Applies filters to grab an image collecton.

        Args:
            collection (str): Which collection to grab images from
            start_date (ee.Date): Start date of filtering
            end_date (ee.Date): End date of filtering
            tRP1 (str): Band to filter for. Defaults to None for None for any bands
            tRP2 (str): Secondary band to filter for. Defaults for None for any bands
            res (str): L, M, or H. Resolution to filter for. Defaults to None (any resolution)
            ins (str): The instrumental mode to filter for. Defaults to None (any mode)
            earliest_first (bool): If set to True, the ee.ImageCollection returned \
                will be sorted s.t. the first ee.Image will be the captured the \
                    earliest. Defaults to False for latest image first.

        Returns:
            sort (ee.ImageCollection): An image collection with the area of geoJSON
            and the specified filters in the args applied.
        """
        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        aoi = self.get_aoi()

        img_set = ee.ImageCollection(collection).filterBounds(aoi).filterDate(start_date, end_date)

        if tRP1 is not None:
            img_set = img_set.filter(ee.Filter.listContains(
                'transmitterReceiverPolarisation', tRP1))
        if tRP2 is not None:
            img_set = img_set.filter(ee.Filter.listContains(
                'transmitterReceiverPolarisation', tRP2))

        if ins is not None:
            img_set = img_set.filter(ee.Filter.eq('instrumentMode', ins))
        if res is not None:
            img_set = img_set.filter(ee.Filter.eq('resolution', res))

        sort = img_set.sort('system:time_start', opt_ascending=earliest_first)
        return sort

    def one_per(self, time_range, collection='COPERNICUS/S1_GRD_FLOAT',
                      start_date=ee.Date(0),
                      end_date=ee.Date(date.today().isoformat()),
                      tRP1=None, tRP2=None, res=None, ins=None):
        """
        Applies filters to create a LIST with one ee.Image per time_range.

        Args:
            time_range (str): day, month, or year. Specifies the approximate \
                time range between photos.
            collection (str): Which collection to grab images from
            start_date (ee.Date): Start date of filtering
            end_date (ee.Date): End date of filtering
            tRP1 (str): Band to filter for. Defaults to None for None for any bands
            tRP2 (str): Secondary band to filter for. Defaults for None for any bands
            res (str): L, M, or H. Resolution to filter for. Defaults to None \
                for any resolution
            ins (str): The instrumental mode to filter for. Defaults to None \
                for any instrument mode

        Returns:
            collected_imgs (ee.ImageCollection): An image collection with the area
            of geoJSON and the proper filters applied
        """
        def percent_missing(image):
            """
            Helper function that returns the % of the image data missing in the first band.

            Args:
                image (ee.Image): The image to calculate the % missing of

            Returns:
                percentMissing (float): The % missing of the image data compared \
                    to the self.get_aoi()
            """
            missing = ee.Number(image.mask().expression('1-b(0)').reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))
            totalArea = ee.Number(ee.Image(1).mask().reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))

            percent_missing = missing.divide(totalArea).getInfo()
            return percent_missing

        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        end_date_time = end_date

        current_start_time = start_date

        collected_imgs = []
        while ee.Algorithms.If(
                ee.Number.expression("x > 0", {
                    'x': end_date_time.difference(current_start_time, 'day')
                    }), 1, 0).getInfo():
            (current_start_time, current_end_time) = (ee.Date(current_start_time)
                                                      .getRange(time_range).getInfo()['dates'])
            img_col = self.apply_filters(collection=collection,
                              start_date=current_start_time,
                              end_date=current_end_time, tRP1=tRP1, tRP2=tRP2,
                              res=res, ins=ins, earliest_first=True)
            try:
                as_list = img_col.toList(img_col.size())
                best = ee.Image(as_list.get(0)).clip(self.get_aoi())
                pm_best = percent_missing(best)
                for i in range(as_list.length().getInfo()):
                    latest = ee.Image(as_list.get(i)).clip(self.get_aoi())
                    pm_latest = percent_missing(latest)
                    if pm_latest < 0.01:
                        best = latest
                        pm_best = pm_latest
                        break
                    elif pm_latest < pm_best:
                        best = latest
                        pm_best = pm_latest
                collected_imgs.append(best.clip(self.get_aoi()))
                print('Selected an image for {}'
                      .format(ee.Date(current_start_time).format('YYYY-MM-dd').getInfo()))

            except:
                print('There are no images in the',
                      time_range, "starting on",
                      ee.Date(current_start_time).format('YYYY-MM-dd').getInfo())
                print('The best image had {:.2f}% pixels of data missing. \
Try selecting a smaller area.'.format(pm_best*100))

            current_start_time = current_end_time

        return collected_imgs

    def latest_img(self, collection='COPERNICUS/S1_GRD_FLOAT', threshold=80):
        """
        Grabs the latest image in the given collection.

        Args:
            collection (str): A collection name from GEE's public collections data. \
                Defaults to S1_GRD_FLOAT

        Returns:
            latest (ee.Image): The latest image for this area
        """
        def validity(image, threshold):
            def percent_missing(image):
                """
                Helper function that returns the % of the image data missing in the first band.
            
                Args:
                    image (ee.Image): The image to calculate the % missing of
            
                Returns:
                    percentMissing (float): The % missing of the image data compared \
                        to the self.get_aoi()
                """
                missing = ee.Number(image.mask().expression('1-b(0)').reduceRegion(
                    ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))
                totalArea = ee.Number(ee.Image(1).mask().reduceRegion(
                    ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))
            
                pm = missing.divide(totalArea).getInfo()

                return pm
            
            return percent_missing(image)*100 < (100 - threshold)
        
        img_col = self.apply_filters(collection=collection)
        eelist = img_col.toList(img_col.size())
        
        for i in range(min(50, img_col.size().getInfo())):
            latest = ee.Image(eelist.get(i)).clip(self.get_aoi())
            if validity(latest, threshold=threshold):
                return latest
                break
        print('No images within threshold')
        return None

    def append_elevation_info(self, image):
        """
        Adds the elevation information to each image passed into it. \
            The image argument must be an ee.Image.
            Warning: this method takes from the mosaic data, so it does not
            vary with time. 

        Args:
            images (ee.Image): Image to add the elevation information.
            Since this is a class function, these are covering the same geographical area.

        Returns:
            multi (ee.Image): Image with added elevation as a new band
        """
        assert isinstance(image, ee.Image), "Image must be a singular ee.Image object"


        elv_collection = 'UMN/PGC/REMA/V1_1/8m'
        aoi = self.get_aoi()

        elevation = ee.Image(elv_collection).clip(aoi)
        multi = ee.Image([image, elevation])
        
        return multi

    def normalize_all_bands(self, image):
        """
        Noramlizes each of the bands in an image to range in values \
            between 0 and 1.

        Args:
            image (ee.Image): Image to normalize

        Returns:
            image_norm (ee.Image): A new image, with normalized float values
            dicts (list): A list of ee.Dictionary containing the min and max \
                of each band.
        """
        assert isinstance(image, ee.Image), "Image must be a singular ee.Image object"

        aoi = self.get_aoi()
        bands = image.bandNames().getInfo()
        img_bands = []
        dicts = []
        for band in bands:
            min_max_dict = image.select(band).reduceRegion(ee.Reducer.minMax(), aoi,
                                                crs='EPSG:3031', scale=1000)

            mini = ee.Number(min_max_dict.get('{}_min'.format(band)))
            maxi = ee.Number(min_max_dict.get('{}_max'.format(band)))

            img_bands.append(image.select(band).unitScale(mini.subtract(1), maxi.add(1)))
            dicts.append(min_max_dict)
        image_norm = ee.Image(img_bands)

        return image_norm, dicts
    
    def segment(self, image, compactness=100, gammafilter=True):
        """
        (Warning: removes the angle band)
        
        Segments an image or images using the Google Earth Engine Algorithm \
            SNIC algorithm
        
        Args:
            images (ee.Image, ee.ImageCollection, list): Image/images to segment
            compactness (int): Number representing the approximate size of clusters
            gammafilter (bool): If enabled, will filter the images before segmentation
            
        Returns:
            segmented (same as images): The image/images with added bands for
            clusters/seeds, and the original bands adjusted to represent the 
            mean in each cluster
        """
        assert isinstance(image, (
            ee.Image, ee.ImageCollection, list)
            ), "Image must be either ee.Image, ee.ImageCollection, or list of ee.Images"
        
        system_index = image.get('system:index').getInfo() + '_segmentation'
        
        if gammafilter:
            image = self.gammafilter(image)
        
        def map_segment(image):
            return ee.Algorithms.Image.Segmentation.SNIC(
                image, **{'compactness': compactness,
                          'connectivity': 8}).set('system:index', system_index)
        def remove_angle(image):
            bands_angle_removed = image.bandNames().filter(
                ee.Filter.neq('item', 'angle'))
            return image.select(bands_angle_removed)
        
        if isinstance(image, ee.Image):
            image = remove_angle(image)    
            segmented = map_segment(image)
        elif isinstance(image, ee.ImageCollection):
            image = self.gammafilter(image)
            segmented = image.map(map_segment)
        elif isinstance(image, list):
            image = self.gammafilter(image)
            segmented = list(map(map_segment, image))
        return segmented
        

    def gammafilter(self, image):
        """
        Applies a gamma maximum filter to an image/images. As implemented as in
        Sentinel-1 SAR Backscatter Analysis Ready Data Preparation in Google Earth Engine

        Args:
            image (ee.Image or ee.ImageCollection): The image/images to be filtered for speckle

        Returns:
            filtered (ee.Image): The filtered image/images

        """
        assert isinstance(image, (
            ee.Image, ee.ImageCollection, list)
            ), "Image must be either ee.Image, ee.ImageCollection, or list of ee.Images"
        
        if isinstance(image, ee.Image):
            filtered = gammamap(image)
        elif isinstance(image, ee.ImageCollection):
            filtered = image.map(gammamap)
        elif isinstance(image, list):
            filtered = list(map(self.gammafilter, image))
        return filtered

    def disp(self, image, rgb=False, band=0):
        """
        Displays an image in rgb/grayscale folium map fashion

        Args:
            image (ee.Image): The image to display
            rgb (bool): Whether or not to display in rgb corresponding to
            band (int): Selects which band to display if rgb is set to False. Defaults to 0

        Returns:
            None.
        """
        assert isinstance(image, ee.Image), "Image must be a singular ee.Image object"

        location = self.get_aoi().centroid().coordinates().getInfo()[::-1]
        # folium doesn't support crs other than crs 4326
        fmap = folium.Map(location=location, zoom_start=12)
        bands = image.bandNames().getInfo()
        if rgb:
            try:
                blue = image.select('elevation')
                blue.bandNames().getInfo()
            except:
                blue = image.select(bands[0]).divide(image.select(bands[1]))

            rgb = ee.Image.rgb(image.select(bands[0]),
                               image.select(bands[1]), blue)
            fmap.add_ee_layer(rgb, {'min': [0, 0, 0], 'max': [1, 1, 200]}, name='Image')
            fmap.add_child(folium.LayerControl())
            display(fmap)

        else:
            fmap.add_ee_layer(image.select(bands[band]), {'min': 0, 'max': 1}, name='Image')
            fmap.add_child(folium.LayerControl())
            display(fmap)

    def download(self, image, scale, cloud_bucket, directory, tryReduce=False):
        """
        Downloads either an image or an image collection to a directory.
        (note: I couldn't get geemap to download singular images, but
        I also couldn't get Google EE to download multiple images. In the end,
        I decided to download singular images to the local directory, but
        python lists of images or ee.ImageCollection will be saved to
        the glaciers_ee bucket in Google Cloud Platform)

        Args:
            images (ee.Image or ee.ImageCollection or list): image/images to download
            directory (str): name of relative directory to save images to,
            leave as a blank string you'd like to save in current directory
            scale (float): The scale to download at in meters/pixel.

        Returns:
            None.
        """
        assert isinstance(image, (
            ee.Image, ee.ImageCollection, list)
            ), "Image must be either ee.Image, ee.ImageCollection, or list of ee.Images"

        if isinstance(image, ee.Image):
            print('When the images are finished uploading, they will be avaiable at:')
            print(f'https://console.cloud.google.com/storage/browser/{cloud_bucket}')
            batchExport([image], scale=scale, cloud_bucket=cloud_bucket,
                        directory=directory, tryReduce=tryReduce,
                        coords=self.get_coords())

        elif isinstance(image, list):
            print('When the images are finished uploading, they will be avaiable at:')
            print(f'https://console.cloud.google.com/storage/browser/{cloud_bucket}')
            batchExport(image, scale=scale, cloud_bucket=cloud_bucket,
                            directory=directory, tryReduce=tryReduce,
                            coords=self.get_coords())

        elif isinstance(image, ee.ImageCollection):
            print('When the images are finished uploading, they will be avaiable at:')
            print(f'https://console.cloud.google.com/storage/browser/{cloud_bucket}')
            aslist = eeICtolist(image)
            batchExport(aslist, scale=scale, cloud_bucket=cloud_bucket,
                            directory=directory, tryReduce=tryReduce,
                            coords=self.get_coords())

    def hist(self, image, band=0):
        """
        Creates the values for an intensity histogram of an image.

        Args:
            image (ee.Image): The image to calculate the histogram for
            band (int): The band to calculate the pixel intensities for

        Returns:
            hist (list): The histogram created
        """
        assert isinstance(image, ee.Image), "Image must be a singular ee.Image object"
        aoi = self.get_aoi()
        bands = image.bandNames()

        band_max = image.select(band).reduceRegion(ee.Reducer.max(),
                                                   aoi, crs='EPSG:3031', scale=100)
        maxi = ee.Number(band_max.get(bands.get(band))).getInfo()
        if maxi >= 2:
            print("Warning: the image may not haven been properly normalized.",
                  "The image should be renormalized before creating a histogram")

        hist = image.select(band).reduceRegion(ee.Reducer.fixedHistogram(0, 1, 500),
                                               aoi).get(bands.get(band)).getInfo()

        return hist

    def get_stats(self, image, band=0):
        """
        Grabs common statistics about and image's specified band including mean, variance, and skew.

        Args:
            image (ee.Image): The image to grab stats about
            band (int): The band to make calculations about of the image

        Return:
            stats (dict): A dictionary containing statistics about the image band.
        """
        assert isinstance(image, ee.Image), "Image must be a singular ee.Image object"
        bands = image.bandNames().getInfo()

        stats = {}
        stats['mean'] = image.select(bands[band]).reduceRegion(ee.Reducer.mean(),
                          self.get_aoi()).get(bands[band]).getInfo()
        stats['variance'] = image.select(bands[band]).reduceRegion(ee.Reducer.variance(),
                          self.get_aoi()).get(bands[band]).getInfo()
        stats['skew'] = image.select(bands[band]).reduceRegion(ee.Reducer.skew(),
                          self.get_aoi()).get(bands[band]).getInfo()
        return stats
    
class CustomCollection(Area):
    """
    This is a subclass of the main class. Use it on importing images from \
        Google Cloud Storage. Standard operations can be applied like 
        gammafilter and segmentation.

    Args: 
        cloud_bucket (str): string describing the name of the cloud bucket
        directory (str): directory describing the directory where the files are stored
        geeusername (str): your username to store the asset in the code editor

    """
    def __init__(self, cloud_bucket, directory, geeusername):
        bucket = client.get_bucket(cloud_bucket)
        blobs = client.list_blobs(bucket)
        assets = []
        
        def all_exists(blobs, directory):
            command = f'earthengine ls users/{geeusername}'
            pop = subprocess.Popen(command, env=os.environ.copy(),
                                shell=True, stdout=subprocess.PIPE)
            output = pop.stdout.read().decode()
            for blob in blobs:

                ind = str(blob).find('/')
                find = ' ' + directory
                if str(blob)[ind-1:ind-len(find)-1:-1] != find[::-1]: 
                    # if directory doesn't match, continue to next iter
                    continue
                
                if str(blob)[ind:str(blob).find(',', ind)].strip() == '/':
                    # if blob is the actual directory and not a file, continue
                     continue
                 
                blob_info = str(blob).split(' ')
                
                assetname = blob_info[2][blob_info[2].find('/')+1:-1]
                if assetname.endswith('.tif'):
                    assetname = assetname[:-4]
                assets.append(assetname)
                

                if (geeusername + '/' + assetname) not in output:
                    return False
            return True
        
        if all_exists(blobs, directory):
            assetlist = ['users/'+geeusername+'/'+assetname for assetname in assets]
            self.eelist = [ee.Image(asset) for asset in assetlist]
        else:
            self.eelist = multicloudtoee(cloud_bucket, directory, geeusername)
        geoJSON = geoJSONer(self.eelist[0].get('system:footprint').getInfo()['coordinates'])
        
        super().__init__(geoJSON)
        
        unbounded = [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]]
        if self.coords == unbounded:
            new = [[[-179, -85],[179, -85],[179, 85],[-179, 85],[-179, -85]]]
            self.coords = new
            self.aoi = ee.Geometry.Polygon(self.coords, proj='EPSG:4326',
                                           geodesic=False, evenOdd=True, maxError=1)
        
    def get_coords(self):
        """
        Gets the coordinates defined by the geoJSON.

        Args:
            None.

        Returns:
            self.coords (list): The coordinates defined by the geoJSON.

        """
            
        return self.coords

    def get_aoi(self):
        """
        Gets the AOI defined by the coordinates.

        Args:
            None.

        Returns:
            self.aoi (list): The AOI defined by the coordinates.

        """
        return self.aoi
    
    def latest_img(self, threshold=80):
        """
        Grabs the latest image in the given collection.

        Args:
            collection (str): A collection name from GEE's public collections data. \
                Defaults to S1_GRD_FLOAT

        Returns:
            latest (ee.Image): The latest image for this area
        """
        
        img_col = self.apply_filters()
        eelist = img_col.toList(img_col.size())
        
        latest = ee.Image(eelist.get(0)).clip(self.get_aoi())
        return latest
    
    def apply_filters(self, start_date=ee.Date(0),
                      end_date=ee.Date(date.today().isoformat()),
                      earliest_first=False):
        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        img_set = ee.ImageCollection(self.eelist)

        sort = img_set.sort('system:time_start', opt_ascending=earliest_first)    
        return sort
    
    def one_per(self, time_range, start_date=ee.Date(0),
                      end_date=ee.Date(date.today().isoformat())):
        """
        Applies filters to create a LIST with one ee.Image per time_range.

        Args:
            time_range (str): day, month, or year. Specifies the approximate \
                time range between photos.
            start_date (ee.Date): Start date of filtering
            end_date (ee.Date): End date of filtering

        Returns:
            collected_imgs (ee.ImageCollection): An image collection with the area
            of geoJSON and the proper filters applied
        """
        def percent_missing(image):
            """
            Helper function that returns the % of the image data missing in the first band.

            Args:
                image (ee.Image): The image to calculate the % missing of

            Returns:
                percentMissing (float): The % missing of the image data compared \
                    to the self.get_aoi()
            """
            missing = ee.Number(image.mask().expression('1-b(0)').reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))
            totalArea = ee.Number(ee.Image(1).mask().reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))

            percent_missing = missing.divide(totalArea).getInfo()
            return percent_missing

        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        end_date_time = end_date

        current_start_time = start_date

        collected_imgs = []
        while ee.Algorithms.If(
                ee.Number.expression("x > 0", {
                    'x': end_date_time.difference(current_start_time, 'day')
                    }), 1, 0).getInfo():
            (current_start_time, current_end_time) = (ee.Date(current_start_time)
                                                      .getRange(time_range).getInfo()['dates'])
            img_col = self.apply_filters(start_date=current_start_time,
                              end_date=current_end_time, earliest_first=True)
            try:
                as_list = img_col.toList(img_col.size())
                best = ee.Image(as_list.get(0)).clip(self.get_aoi())
                pm_best = percent_missing(best)
                for i in range(as_list.length().getInfo()):
                    latest = ee.Image(as_list.get(i)).clip(self.get_aoi())
                    pm_latest = percent_missing(latest)
                    if pm_latest < 0.01:
                        best = latest
                        pm_best = pm_latest
                        break
                    elif pm_latest < pm_best:
                        best = latest
                        pm_best = pm_latest
                collected_imgs.append(best.clip(self.get_aoi()))
                print('Selected an image for {}'
                      .format(ee.Date(current_start_time).format('YYYY-MM-dd').getInfo()))

            except:
                print('There are no images in the',
                      time_range, "starting on",
                      ee.Date(current_start_time).format('YYYY-MM-dd').getInfo())
                print('The best image had {:.2f}% pixels of data missing. \
Try selecting a smaller area.'.format(pm_best*100))

            current_start_time = current_end_time

        return collected_imgs

class CustomImage(Area):
    def __init__(self, cloud_bucket, directory, assetname, geeusername):
        if assetname.endswith('.tif'):
            assetname = assetname[:-4]
        
        command = f'earthengine ls users/{geeusername}'
        pop = subprocess.Popen(command, env=os.environ.copy(),
                            shell=True, stdout=subprocess.PIPE)
        if (geeusername + '/' + assetname) not in pop.stdout.read().decode():
            self.eeImage = cloudtoeecommand(cloud_bucket, directory,
                                            assetname, geeusername)
        else:
            self.eeImage = ee.Image(('users/' + geeusername + '/' + assetname))
        
        time.sleep(3)
        
        geoJSON = geoJSONer(self.eeImage.get('system:footprint').getInfo()['coordinates'])
        super().__init__(geoJSON)
    def get_image(self):
        return self.eeImage
    def latest_img(self):
        return self.get_image()
    def apply_filters(self):
        return ee.ImageCollection(self.get_image())
    def one_per(self):
        return [self.get_image(),]
       
# yay
