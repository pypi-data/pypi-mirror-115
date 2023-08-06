import subprocess,os,sys,logging
from vmrunPacked.util import *

class Pack:
    def __init__(self,vmxFilePath,userName=str(),passWord=str(),product=WS):
        self.vmxFilPpath = vmxFilePath
        self.userName = userName
        self.passWord = passWord
        self.vmProduct = product

        self.vmrun_exec = self.find_exec_path()
        if self.vmrun_exec is None:
            logging.info("can't find vmrun path !.")

    def find_exec_path(self):
        try:
            VMRUN_PATH = None
            if sys.platform == WIN32:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                try:
                    registry_path = winreg.OpenKey(registry,NAME_OF_VMWARE)
                    try:
                        vmware_path = winreg.QueryValueEx(registry_path,INSTALL_PATH)[0]
                    finally:
                        winreg.CloseKey(registry_path)
                finally:
                    registry.Close()

                if vmware_path != str():
                    VMRUN_PATH = vmware_path + VMWARE_EXE
            else:
                get_line_path = os.environ.get(PATH)
                if get_line_path is not None:
                    for item_exec in get_line_path.split(os.pathsep):
                        exec_path = os.path.join(item_exec,VMRUN)
                        if os.path.isfile(exec_path):
                            VMRUN_PATH = exec_path.replace(' ', '\\ ')
                            break
            return VMRUN_PATH
        except Exception as e:
            logging.debug(e)

    def start(self):
        try:
            msg = [START]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def __exec__(self,types,ext=False):
        try:
            command = types.pop(0)
            parameters = " ".join(types)
            fit_cmd = f"{self.vmrun_exec} -T {self.vmProduct} -gu {self.userName} -gp {self.passWord} {command} {self.vmxFilPpath} {parameters}"
            
            if ext:
                fit_cmd = f"{self.vmrun_exec} {command}"

            if sys.platform != WIN32:
                exec_cli = [SH, ARGS_C, fit_cmd]
            else:
                exec_cli = fit_cmd
            
            logging.debug(exec_cli)
            out = subprocess.Popen(exec_cli, stdout=subprocess.PIPE)
            
            return out.stdout.readlines()
        except Exception as e:
            logging.debug(e)

    def stop(self,soft=False,hard=False):
        try:
            msg = [STOP]
            status = self.check_soft_hard(soft,hard)
            if status is not None:
                msg.append(status)
            self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def check_soft_hard(slef,s_b,h_b):
        try:
            bRet = None
            if s_b and h_b:
                bRet = SOFT
            elif s_b:
                bRet = SOFT
            elif h_b:
                bRet = HARD
            return bRet
        except Exception as e:
            logging.debug(e)

    def reset(self,soft=False,hard=False):
        try:
            msg = [RESET]
            status = self.check_soft_hard(soft,hard)
            if status is not None:
                msg.append(status)
            self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def suspend(self,soft=False,hard=False):
        try:
            msg = [SUSPEND]
            status = self.check_soft_hard(soft,hard)
            if status is not None:
                msg.append(status)
            self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def pause(self):
        try:
            msg = [PAUSE]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def unpause(self):
        try:
            msg = [UNPAUSE]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    ########################################
    # Snapshot Commands
    #######################################

    def list_snap_shots(self):
        try:
            msg = [LIST_SNAP_SHOTS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def snapshot(self,snap_shot_name):
        try:
            msg = [SNAP_SHOT,snap_shot_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)
    
    def delete_snapshot(self,snap_shot_name):
        try:
            msg = [DELETE_SNAP_SHOT,snap_shot_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def revert_to_snap_shot(self,snap_shot_name):
        try:
            msg = [REVERT_TO_SNAP_SHOT,snap_shot_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    #############################################
    # RECORD/REPLAY COMMANDS
    #############################################

    def begin_recording(self,snap_name):
        try:
            msg = [BEGIN_RECORDING,snap_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def end_recording(self):
        try:
            msg = [END_RECORDING]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def begin_replay(self,snap_name):
        try:
            msg = [BEGIN_REPLAY,snap_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def end_replay(self):
        try:
            msg = [END_REPLAY]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    #######################################
    # GUEST OS COMMANDS
    #######################################

    def run_program_in_guest(self,program_file,*program_args,noWait=False,activeWindow=False,interactive=False):
        try:
            msg = [RUN_PROGRAM_IN_GUEST]
            if noWait:
                msg.append(NO_WAIT)
            if activeWindow:
                msg.append(ACTIVE_WINDOW)
            if interactive:
                msg.append(INTER_ACTIVE)
            msg.append(program_file)
            msg.append(" ".join(list(program_args)))
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def file_exists_in_guest(self,file_path):
        try:
            msg = [FILE_EXISTS_IN_GUEST,file_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def set_shared_folder_state(self,share_name,new_path,readonly=True,writable=False):
        try:
            msg = [SET_SHARED_FOLDER_STATE,share_name,new_path]
            if readonly and writable:
                msg.append(WRITABLE)
            elif readonly:
                msg.append(READ_ONLY)
            elif writable:
                msg.append(WRITABLE)
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def add_shared_folder(self,share_name,host_path):
        try:
            msg = [ADD_SHARED_FOLDER,share_name,host_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def remove_shared_folder(self,share_name):
        try:
            msg = [REMOVE_SHARED_FOLDER,share_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def enable_shared_folders(self):
        try:
            msg = [ENABLE_SHARED_FOLDERS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def disable_shared_folders(self):
        try:
            msg = [DISABLE_SHARED_FOLDERS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)
    
    def list_processes_in_guest(self):
        try:
            msg = [LIST_PROCESS_IN_GUEST]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def kill_process_in_guest(self,pid):
        try:
            msg = [KILL_PROCESS_IN_GUEST,pid]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def run_script_in_guest(self,interpreter_path, script_path):
        try:
            msg = [RUN_SCRIPT_IN_GUEST,interpreter_path,script_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def delete_file_in_guest(self,file_path):
        try:
            msg = [DELETE_FILE_GUEST,file_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def create_directory_in_guest(self,dir_path):
        try:
            msg = [CREATE_DIR_IN_GUEST,dir_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def delete_directory_in_guest(self,dir_path):
        try:
            msg = [DELETE_DIR_IN_GUEST,dir_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def list_directory_in_guest(self,dir_path):
        try:
            msg = [LIST_PROCESS_IN_GUEST,dir_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def copy_file_from_host_to_guest(self,host_path,guest_path):
        try:
            msg = [COPY_FILE_FROM_HOST_TO_GUEST,host_path,guest_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def copy_file_from_guest_to_host(self,guest_path,host_path):
        try:
            msg = [COPY_FILE_FROM_GUEST_TO_HOST,guest_path,host_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def rename_file_in_guest(self,old_name,new_name):
        try:
            msg = [RENAME_FILE_IN_GUEST,old_name,new_name]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def capture_screen(self,host_path):
        try:
            msg = [CAPTURE_SCREEN,host_path]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def write_variable(self,val_name,val_value,runtimeConfig=False,guestEnv=False):
        try:
            msg = [WRITE_VARIABLE]
            if runtimeConfig and guestEnv:
                pass
            elif runtimeConfig:
                msg.append(RUN_TIME_CONFIG)
            elif guestEnv:
                msg.append(GUEST_ENV)
            msg.append(val_name,val_value)
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def read_variable(self,val_name,runtimeConfig=False,guestEnv=False):
        try:
            msg = [READ_VARIABLE]
            if runtimeConfig and guestEnv:
                pass
            elif runtimeConfig:
                msg.append(RUN_TIME_CONFIG)
            elif guestEnv:
                msg.append(GUEST_ENV)
            msg.append(val_name)
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    ###############################################
    # VPROBE COMMANDS
    ###############################################

    def vprobe_version(self):
        try:
            msg = [VPROB_VERSION]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def vprobe_load(self,script):
        try:
            msg = [VPROB_LOAD,script]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def vprobe_load_file(self,vp):
        try:
            msg = [VPROB_LOAD_FILE,vp]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def vprobe_reset(self):
        try:
            msg = [VPROB_RESET]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def vprobe_list_probes(self):
        try:
            msg = [VPROB_LIST_PROBES]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def vprobe_list_globals(self):
        try:
            msg = [VPROB_LIST_GLOBALS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    #######################################
    # GENERAL COMMANDS
    #######################################

    def list_vm(self):
        try:
            msg = [LIST]
            return self.__exec__(msg,ext=True)
        except Exception as e:
            logging.debug(e)

    def upgrade_vm(self):
        try:
            msg = [UPGRADEVM]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def install_tools(self):
        try:
            msg = [INSTALL_TOOLS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def register(self):
        try:
            msg = [REGISTER]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def un_register(self):
        try:
            msg = [UNREGISTER]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def list_registered_vm(self):
        try:
            msg = [LIST_REGISTER_VM]
            return self.__exec__(msg,ext=True)
        except Exception as e:
            logging.debug(e)
    
    def delete_vm(self):
        try:
            msg = [DELETE_VM]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def clone(self,dest_vmx,snap_name,full=False,linked=False):
        try:
            msg = [CLONE,dest_vmx]
            if full and linked:
                msg.append(FULL)
            elif full:
                msg.append(FULL)
            elif linked:
                msg.append(LINKED)
            msg.append(snap_name)
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)

    def get_guest_ip_address(self):
        try:
            msg = [GET_GUEST_IP_ADDRESS]
            return self.__exec__(msg)
        except Exception as e:
            logging.debug(e)