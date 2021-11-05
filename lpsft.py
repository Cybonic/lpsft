import os
import argparse
import tempfile
from os import walk

# server      = "193.136.205.249"
# server      = "192.168.0.113"
#server      ='tiago-deep'
#passward    = 'btph1312'
# usr         = 'tiago'



subflag = '-b'

IGNORE_FILE = '.gitignore'

def split(text):

    op= ['\\','/']
    out = ''
    for o in op:
        split = text.split(o)
        if len(split)>1:
            out =  split
    if out == '':
        out = split 
    return(out)


def get_items(path):
     # Load from ignore files item to ignore
    files_to_ignore = []
    for file in open(IGNORE_FILE,'r'):
        file = file.strip().strip('*').strip('/')
        files_to_ignore.append(file)
    # Add files and dir that not to send at any circumstances  
    files_to_ignore.extend(['.gitignore'])
    files_to_ignore.extend(['.git'])

    files,dirs = get_valide_items(path,files_to_ignore)

    return(files,dirs)

def get_valide_items(path,files_to_ignore):
    '''
    
    
    '''
    # Get the package name 
    root_name = path.split(os.sep)[-1]
    # Run trough all files and directories 
    files = []
    dirs = []
    for (dirpath, dirnames, filenames) in walk(path):
        # Find the position of the package in the global path
        index  =  [idx for idx,st in enumerate(dirpath.split(os.sep)) if st in root_name][0]
        # Get the relative path begining at the root package  
        sub_folder_list = dirpath.split(os.sep)[index+1:]
        
        files.extend([file for file in filenames if not file in files_to_ignore])

        dirs.extend([dirname for dirname in dirnames if not dirname in files_to_ignore])
        # if len(sub_folder_list)>0: # Only if there is one or more folder 
            # Check only the folders at the package' root location
        #    if sub_folder_list[0] in files_to_ignore:  
        #        continue
        #    dirs.extend([os.path.join(sub_folder_list[0])])
        #else:
            # This way only files that are at the package's root are added 
            
        break
    return(files,dirs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("./infer.py")
    parser.add_argument(
      '-t',
      type=str,
      default = "send",
      required=False,
      help='flag which defines flow direction: send or receive ',
    )

    parser.add_argument(
      '-f',
      type=str, 
      default = "update.txt",
      required=False,
      help='Dataset to train with. No Default',
    )

    parser.add_argument(
      '-dst',
      type=str,
      default = "D:\\worksapace",
      required=False,
      help='Dataset to train with. No Default',
    )
    parser.add_argument(
      '-s',
      type=str,
      default = "tiago-deep",
      required=False,
      help='destination IP address',
    )
    parser.add_argument(
      '-u','--usr',
      type=str,
      default = "tiago",
      required=False,
      help='remote user name',
    )
    parser.add_argument(
      '-p','--pas',
      type=str,
      default = "btph1312",
      required=False,
      help='remote passwoard',
    )

    FLAGS, unparsed = parser.parse_known_args()

    print("[INF] File: " + FLAGS.f)
    print("[INF] Server: "+ FLAGS.s)
    print("[INF] User: "+ FLAGS.usr)
    print("[INF] Password: " + FLAGS.pas)

    # Login
    user_login  = FLAGS.usr + "@" + FLAGS.s
    pass_login  =' '.join(['-pw',FLAGS.pas]) 
    login       = ' '.join([user_login,pass_login])
    psftp_cmd         = 'psftp'


    current_root = os.getcwd()

    fd, path = tempfile.mkstemp()
    remote = {'root': '' ,'files':[],'dir':[]}
    files = []

    print("[INF] Operation: " + FLAGS.t)
    if not os.path.isfile(FLAGS.f):
        print("[ERR] File does not exist: " + FLAGS.f)
        exit(0)

    
    
    absolute_path = os.path.join(current_root,FLAGS.f)
    print("[WARN] Path " + absolute_path)
    # local file parsing
    for line in open(absolute_path,'r'):
        print("[DEBUG] line: " + line) 
        line = line.strip()
        if '$root' in line:
            remote['root'] = line.split('=')[1]
            #remote_path = 
        elif '#' in line:
            continue 
        elif "$all" in line:
            # update all valide items (ie, files and folder)
            files,dirs = get_items(current_root)
            remote['files'] = files
            remote['dir'] = dirs
            print(remote)
             
        else:
            if os.path.isfile(line):
                remote['files'].append(line)
            if os.path.isdir(line):
                remote['dir'].append(line)

    # destination file code building  
    try:
        with os.fdopen(fd, 'w') as tmp:

            if remote['root'] != '':
                cmd = 'cd'
                remote_cmd = ' '.join([cmd,remote['root']])
                tmp.write(remote_cmd + '\n')

            if FLAGS.t == "send" :    
                cmd = 'put' 
            elif FLAGS.t == "receive":
                cmd = 'get'

            for f in remote['files']:
                remote_cmd = ' '.join([cmd,f,f])
                
                tmp.write(remote_cmd + '\n')
            
            for f in remote['dir']:
                #absolute_file = os.path.join(current_root,f) 
                #print(absolute_file)
                remote_cmd = ' '.join([cmd,'-r',f,f])
                tmp.write(remote_cmd + '\n')
            
        
        # Login to remote 
        # Run cmds in remote
        terminal = ' '.join([psftp_cmd,login,subflag,path])
        os.system(terminal)
    finally:
        os.remove(path)



