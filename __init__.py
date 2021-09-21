import sys
import pathlib
import os
import numpy as np

package_name = "rattnet"
path = str(pathlib.Path(__file__).parent.absolute()).split(os.sep)

matching = np.array([i for i,s in enumerate(path) if package_name == s]).item()
package_root_path = os.sep.join(path[:matching+1])

directories = [os.path.join(package_root_path,d) for d in os.listdir(package_root_path) if os.path.isdir(os.path.join(package_root_path,d))]
sys.path.append(directories)
