import os
import argparse
import tempfile

# server      = "193.136.205.249"
server      = "192.168.0.106"
passward    = 'btph1312'
usr         = 'tiago'

user_login  = usr + "@" + server
pass_login  =' '.join(['-pw',passward]) 
login       = ' '.join([user_login,pass_login])
psftp_cmd         = 'psftp'

subflag = '-b'


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
      default = "psftp/update.txt",
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

    FLAGS, unparsed = parser.parse_known_args()

    fd, path = tempfile.mkstemp()
    remote = {'root': '' ,'files':[],'dir':[]}
    files = []

    print("[INF] Operation: " + FLAGS.t)
    if not os.path.isfile(FLAGS.f):
        print("[ERR] File does not exist: " + FLAGS.f)
        exit(0)

    print("[INF] Loaded File: " + FLAGS.f)

    # local file parsing
    for line in open(FLAGS.f,'r'):
        
        line = line.strip()
        if '$root' in line:
            remote['root'] = line.split('=')[1]
            #remote_path = 
        elif '#' in line:
            continue 
        elif "$all" in line:
            # update everything 
            print("[WARN] Not implemented")
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
                remote_cmd = ' '.join([cmd,'-r',f,f])
                tmp.write(remote_cmd + '\n')
            
        
        # Login to remote 
        # Run cmds in remote
        terminal = ' '.join([psftp_cmd,login,subflag,path])
        os.system(terminal)
    finally:
        os.remove(path)



