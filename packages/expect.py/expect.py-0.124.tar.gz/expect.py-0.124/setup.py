class Var:
      nameA='expect.py'
      nameB='0.124'
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
         
          if  name!=None and vvv!=None:
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    R[1]=f"      nameA='{name}'\n"
                    R[2]=f"      nameB='{vvv}'\n"
                    ##########################
                    f.seek(0,0)       ## 規0
                    f.writelines(R)
              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  # print( NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            # 'echo >/content/cmd.py/cmds/__init__.py',
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: Moon@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
          for i in cls.text:
              cls.popen(i)
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)


class init(Var):
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= cls.dir
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
                                  
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
          else:
                print("警告: 參數或型別 出現問題") 


class sdist(MD,PIP,init):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"
      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          import os

          print("!XXXXX:" ,os.getcwd() )
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          
          if os.path.isdir("dist"):
            print("@刪除 ./dist")
            ##### os.system(f"rm -rf ./dist")
            os.system(f"rm -rf {os.getcwd()}{os.path.sep}dist")
          ##
          info = [i for i in os.listdir() if i.endswith("egg-info")]
          if  len(info)==1:
              if os.path.isdir( info[0] ):
                 print(f"@刪除 ./{info}")
                 #  os.system(f"rm -rf ./{info[0]}")
                 os.system(f"rm -rf {os.getcwd()}{os.path.sep}{info[0]}")
                
          ##############################################################
          CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist"
         
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = f"twine upload --skip-existing  {os.getcwd()}{os.path.sep}dist{os.path.sep}*"
              # print("@222@",cls.popen(CMD))
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)
          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    # os.system("python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                   
                    ## 結束 ##
                    BLFF="結束."
           
          return  this
          



################################################# 這裡是??????      
import sys
if len(sys.argv)==3 :
         
    Var(sys.argv[1],sys.argv[2])

    import os
    sdist(os.path.dirname(sys.argv[0]))





#############################################
import site
print("pip@",id(site), Var.nameA , Var.nameB )
#############################################



if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':

    ##############################################
    from setuptools.command.install import install
    #####
    from subprocess import check_call
    class PostCMD(install):
          """cmdclass={'install': XXCMD,'install': EEECMD }"""
          def  run(self):
                

                ############
                ############
                import sys
                print("@!@!A",__file__,sys.argv)
                install.run(self)
                print("@!@!B",__file__,sys.argv)

                import site
                print("@run: ",id(site))

                import site
                print("@@@[setup.py]--[site]:",id(site))
                import atexit                
                # def  cleanup_function():
                def  cleanup_function(siteOP):
                    ###########################
                    # %cd /content
                    import os
                    if not os.path.isfile('/content/expect.txt'):
                        os.system("apt-get -qq -y install tcl    >  expect.txt")
                        os.system("apt-get -qq -y install expect  >>  expect.txt")
                        # !apt-get -qq -y install tcl    >  expect.txt 
                        # !apt-get -qq -y install expect  >>  expect.txt  


# !git config --global user.name "moon-start"
# !git config --global chmod.x "moon-start"
###
# import os
# os.popen("git config --global chmod.file").read().rstrip("\n")
#os.system("chmod +x /content/ca.sh")


                    #!/bin/sh
                    text='''#!/usr/bin/python

import os,sys
if len(sys.argv)==2:
  SS=sys.argv[1]
  os.system( "chmod +x "+sys.argv[1]  )
     


                    '''
                    open("/usr/bin/batX","w").write(text)
                    os.system(f"chmod +x /usr/bin/batX")

                    
                    #!/bin/sh
                    text='''#!/usr/bin/python
# -*- coding: UTF-8 -*-

def baseOS(name,pic):
    import base64,os
    # picA="/root/.ssh/id_rsa"
    # picB="/root/.ssh/id_rsa.pub"
    if os.path.isfile(pic):  
        image = open(pic, 'rb')
        value = base64.b64encode(image.read()).decode()
        os.system('git config --global {name} "'+ value +'"')
    else:
        print("沒有 ssh key")


## 宣告
if not len(os.popen("git config --global shh.key").read()):
    baseOS("shh.key","/root/.ssh/id_rsa")
    baseOS("shh.pub","/root/.ssh/id_rsa.pub")
    print("[git config --global shh.key] : ",os.popen("git config --global shh.key").read())
    print("[git config --global shh.pub] : ",os.popen("git config --global shh.pub").read())
else:
    print("[git config --global shh.key] : ",os.popen("git config --global shh.key").read())
    print("[git config --global shh.pub] : ",os.popen("git config --global shh.pub").read())
     
                    '''
                    open("/usr/bin/git-key","w").write(text)
                    os.system(f"chmod +x /usr/bin/git-key")

                    ####
                    ####
                    text='''#!/usr/bin/expect -f
# spawn echo {*}$argv
# eval spawn ssh-keygen -t rsa -b 2048 -C "rsa key"
# spawn sudo chmod 0600 /etc/docker/server-key.pem /etc/docker/server-cert.pem /etc/docker/ca-key.pem /etc/docker/ca.pem


# !rm -rf /root/.ssh/id_rsa
# !rm -rf /root/.ssh/id_rsa.pub
spawn rm -rf /root/.ssh/id_rsa
    expect eof 
spawn rm -rf /root/.ssh/id_rsa.pub
    expect eof 

spawn ssh-keygen -t rsa -b 2048 -C "rsa key" 
    ####################################################
    expect "Enter file in which to save the key"
    send "\n" 
    ####################################################
    expect "Enter passphrase"
    send "\n" 
    ####################################################
    expect "Enter same passphrase again"
    send "\n" 
    expect eof 

spawn git-key
    expect eof 
'''

                    open("/usr/bin/git-ssh","w").write(text)
                    os.system(f"chmod +x /usr/bin/git-ssh")
                    os.system(f"git-ssh")    



                    # import sys,os
                    # # @@ [DIR 1] : build
                    # print("@@ [DIR 1] :",os.popen(f'ls {sys.argv[0][0:-9]}/cmds').read()) ## 錯誤
                    # # os.chdir(sys.argv[0])
                    # # print("[@]",os.popen("ls -al").read())
                    # # os.system("ls -al")
                    # import setupB as B
                    # #### if ("builtins"==__name__):
                    # # exec(open( B.__file__ , encoding = 'utf-8').read(),{"siteOP":siteOP}) 
                    # cmds.setupB
                    # # /usr/local/lib/python3.7/dist-packages
                    # exec(open( f"{siteOP()}{os.path.sep}{Var.nameA}{os.path.sep}setup.py , encoding = 'utf-8').read(),{"siteOP":siteOP}) 
                    

                        
                
                ################################################################################################
                def siteOP():
                    import os,re
                    pip=os.popen("pip show pip")
                    return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
                
                import site
                atexit.register(cleanup_function,siteOP())
                # atexit.register(cleanup_function,site)
                ######################################
                
            

    

            



    ################################################
    # with open("/content/QQ/README.md", "r") as fh:
    # with open("README.md", "r") as fh:
    #           long_description = fh.read()


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    setup(
          # name  =  "cmd.py"  ,
          name  =   f"{Var.nameA}"  ,
          
          ## version
          ## 0.7 0.8 0.9版 3.4版是內建函數寫入   錯誤版笨
          # version= "5.5",
          version=  f"{Var.nameB}"  ,
          # version= f"{Var.name}",
          # version= "01.01.01",
          # version="1.307",
          # name  =  "cmd.py"  ,
          # version= "1.0.4",
          description="My CMD 模組",

          
          #long_description=long_description,
          long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
          long_description_content_type="text/markdown",
          # author="moon-start",
          # author_email="login0516mp4@gmail.com",
          # url="https://gitlab.com/moon-start/cmd.py",
          license="LGPL",
          ####################### 宣告目錄 #### 使用 __init__.py
          ## 1 ################################################ 
          # packages=find_packages(include=['cmds','cmds.*']),
          packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*',"setupB.py"]),    
          ## 2 ###############################################
          # packages=['git','git.cmd',"git.mingw64"],
          # packages=['cmds'],
          # packages = ['moonXP'],
          # package_data = {'': ["moon"] },
          #################################
          # package_data = {"/content" : ["/content/cmd.py/cmds/__init__.py"]},
          #################################
          # data_files=[
          #       # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #       # ('config', ['cfg/data.cfg']),
          #       ( siteD , ['books/siteR.py'])
          # ],
          #################################
          # data_files=[
          #         # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #         # ('config', ['cfg/data.cfg'])
          #         ############ /content/cmd.py
          #         # ('/content', ['cmds/__init__.py'])
          #         ('', ['cmds/__init__.py'])
          # ],
          

          ## 相對路徑 ["cmds/AAA.py"] 壓縮到包裡--解壓縮的依據
          # !find / -iname 'AAA.py'
          # /usr/local/lib/python3.7/dist-packages/content/AAA.py
          # data_files=[
          #         # (f"/{sdist.dir}", ["books/siteR.py"])
          #         (f"{ siteD }", ["books/siteR.py"])
          # ],
          # data_files=[
          #   (r'Scripts', ['bin/pypi.exe']),
          #   (r'Scripts', ['bin/pypi-t.exe'])
          #   # (r'/', ['bin/git.exe'])
          # ],
          ## 安裝相關依賴包 ##
          # install_requires=[
          #     # ModuleNotFoundError: No module named 'apscheduler'
          #     'apscheduler'
              
          #     # 'argparse',
          #     # 'setuptools==38.2.4',
          #     # 'docutils >= 0.3',
          #     # 'Django >= 1.11, != 1.11.1, <= 2',
          #     # 'requests[security, socks] >= 2.18.4',
          # ],
          ################################
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          }
          #########################
    )
   

### B版
# 6-13