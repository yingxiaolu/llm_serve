from flaskr import app

if __name__ == '__main__':
    #flask内置的开发服务器, 单线程开发调试用, 不适用于生产环境. 生成环境代码见Dockerfile
    app.run(host='0.0.0.0', port=5002, debug=True)
