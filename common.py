import os,subprocess,sys
import platform
import shutil
from numpy import ceil
# import pathlib
#sambaServer = '\\\\192.168.1.40\\S\\'
sambaServer = 'S:\\'

versions = ['C2','C3']
versionUpdateTag = '_to_{}'.format(versions[1])

landscapesMap = {
    'AA2': 'AA3',
    'Arequipa_Peru':'Arequipa_Peru3',
    'Atacama_C2': 'Atacama3',
    'Cajamarca_Peru': 'Cajamarca_Peru3',
    'Centro_Italia': 'Centro_Italia3',
    'Colorado_C2': 'Colorado_V3x',
    'Coquimbo_SanJuan': 'CoquimboSanJuan3',
    'Cuzco_Peru': 'Cuzco_Peru3',
    'Husacaran_Peru': 'Huascaran_Peru3',
    'Lima_Peru': 'Lima_Peru3',
    'North-UK2': 'United Kingdom3',
    'Pumalin_Park': 'Pumalin_Park3',
    'Scotland3': 'United Kingdom3',
    'Scotland4': 'United Kingdom3',
    'Slovenia2': 'Slovenia3',
    'South East UK3': 'United Kingdom3',
    'Talca_Los_Andes': 'TalcaLosAndes3',
    'Temuco_Los_Andes': 'TemucoLosAndes3',
    'Transandino': 'Transandino3',
    'United Kingdom': 'United Kingdom3',
    'West_Balkans': 'West_Balkans3',
    'West_Balkans2': 'West_Balkans3',
    'West_Patagonia': 'West_Patagonia3',
    'West-UK': 'United Kingdom3',
    'West-UK2': 'United Kingdom3',
    'France Champagne': 'Fr_ChampagneC3',
    '': '',
}

keepC2 = [  #of those that aren't in landscapesMap
    'AlleghenyRidges',
    'Arizona2',
    'Baja_California',
    'BigPyrenees2',
    'CA',
    'Cascade Range',
    'Christchurch',
    'Colorado_C2',
    'Guatemala',
    'Invermere',
    'Logan2',
    'NW_Montana',
    'Nephi',
    'New_Zealand',
    'Oahu',
    'Ridge-NSW-2',
    'RockyMountains-2',
    'Sierra_Nevada',
    'SoCal2',
    'South_Nevada2',
    'Southern-Alberta',
    'SouthernNorway4',
    'Truckee',
    'West_Patagonia',
    'Wurtsboro',
    'Yellowstone_Park'
]

def subPopenTry(cmd):
    try:
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,shell=True)
        output, error = proc.communicate()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, proc.args, output=output, stderr=error)
        outputLines = output.splitlines()
        return outputLines
    except subprocess.CalledProcessError as e:
        sys.exit('Stop: Error output: {} on cmd "{}"'.format(e.stderr, ' '.join(cmd)))
        return e.stderr

def pathWinLin(path):
    linuxPathStart = '/mnt/'
    winDrives = ['A','C','D','F','S'] #including S means sambaserver path won't be used
    winSambaDrive = sambaServer  # includes Samba windows mapped drive
    list = path.split(os.sep)
    driveLetter = list[0]
    if platform.system() == 'Windows':
        if driveLetter.upper() in winDrives:
            list[0] += ':'
            path = os.sep.join(list)
        elif winSambaDrive not in path:
            path = winSambaDrive + path
    elif linuxPathStart not in path:
        path = linuxPathStart + path
    return path

def rmSlash(path):
    return path.replace('\\\\','\\')

#def linkWinLin(truePath, linkPath):
 #   cmd = 'mklink /d {} {}'.format(rmSlash(linkPath), rmSlash(truePath))
  #  print('true {} <-> link {}'.format(truePath, linkPath))
   # if not os.path.exists(linkPath):
    #    if platform.system() == 'Windows':
     #       cmd = ['mklink', '/d', os.path.join(linksDir, item), os.path.join(trueDir, item) ]
      #  else:
       #     cmd = ['ln', '-s', os.path.join(trueDir, item), os.path.join(linksDir, item)]
        #os.system(cmd)

def buildDirs(finalPath):
    list = finalPath.split(os.sep)
    path = list[0] + os.sep
    for segment in list[1:]:
        path = os.path.join(path,segment)
        if not os.path.exists(path):
            os.mkdir(path)
    if path != finalPath:
        sys.exit('Stop...buildDirs failed. You might need to add the windows drive letter to pathWinLin')


def renameDirsWithTag(dirsList,tags,tagReplacement):
    for dir in dirsList:
        for tag in tags:
            if tag in dir:
                newName = dir.replace(tag,tagReplacement)
                renameTry(dir, newName)

def readfile(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines() #strips the lines of \n
    return lines

def readfileNoStrip(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines(True) #keeplinebreaks=True.  Does not strip the lines of \n
    return lines

def writefile(lines,filepath): #need to have \n's inserted already
    file1 = open(filepath,'w')
    file1.writelines(lines)
    file1.close()
    return

def safeDivide(numerator,denominator):
    if denominator > 0:
        return ceil(numerator/denominator)
    else:
        return 0

def renameTry(oldname, newname):
    shutil.move(oldname, newname)
    print('Renamed {} to {}'.format(oldname, newname))

def makeLink(truePath,linkPath):
    if os.path.islink(linkPath):
        os.remove(linkPath)
    if not os.path.exists(linkPath):
        # try:
            os.symlink(truePath, linkPath)
            # os.system('mklink /d "{}" "{}"'.format(, truePath))
            print('Created link {} -> true {}'.format(linkPath,truePath))
        # except:
        #     print('Problem creating true {} <-> link {}'.format(truePath,linkPath))



def copy_file_to_guest(vm_name, host_file_path, guest_file_path,usernm,passwd):
    """Copies a file from host to guest using VBoxManage."""
    cmd = [
        "vboxmanage",
        "guestcontrol",
        vm_name,
        "copyto",
        host_file_path,
        guest_file_path,
        '--username={}'.format(usernm),
        '--password={}'.format(passwd)
    ]
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print(e.output)

def listRunningVms():
    cmd = [
        "vboxmanage",
        "list",
        "runningvms"
    ]
    result = subprocess.check_output(cmd)
    outputLines = result.decode('utf-8').split('\n')
    return outputLines

def dirSize(path):
    # This suggestion is very slow: sum(f.stat().st_size for f in pathlib.Path(path).glob('**/*') if f.is_file())
    if platform.system() == 'Linux':
        size = subprocess.run(["du", "-s", path], stdout=subprocess.PIPE, text=True).stdout.split('\t')[0]
    else:
        size = 0
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    size += entry.stat().st_size
                elif entry.is_dir():
                    size += dirSize(entry.path)
    return size

def checkAdminRights():
    import ctypes, os
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def getOKor(action,string):
        response = 'None'
        while response.lower() not in ['y','ok']:
            print('\n {}'.format(string))
            response = input('Y,OK/N: ')
            if response.lower() == 'n':
                if action == 'break':
                    break
                elif action == 'continue':
                    continue
                elif action == 'stop':
                    sys.exit('Stop')
                else:
                    sys.exit('Cannot parse action in getOKor:', action)

def getLandPaths(topLandDirs, versionUpdateTag, args):
    from more_itertools import sort_together
    '''Gets landscapes names and paths from dirs with Textures subdir'''
    allLands = []
    allLandPaths = []
    for topDir in topLandDirs:
        items = os.listdir(topDir)
        for item in items:
            itemPath = os.path.join(topDir, item)
            if (not os.path.isdir(itemPath)) or  ('Textures' not in os.listdir(itemPath) or versionUpdateTag in item):
                continue # note: isdir is true for a link pointing to a dir
            if args.omit and ('WestGermany3' in item or 'Slovenia' in item ):
                continue
            if not item in allLands:
                allLands.append(item)
                allLandPaths.append(itemPath)
                cupFile = os.path.join(itemPath,item+'.cup')
                if not os.path.exists(cupFile) and 'Textures' in os.listdir(itemPath): #.cup file required for COTACO task converter
                    os.system('echo "name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,descr \n" > {}'.format(cupFile))
                    print('created', cupFile)

    allLands, allLandPaths = sort_together([allLands, allLandPaths],reverse=args.reverse)
    return allLands, allLandPaths