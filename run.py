# @Time    : 2020/11/18 19:32 
# @Author  : 孙北晨 
# @Version : V 0.1
# @Int     :
from app import create_app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)