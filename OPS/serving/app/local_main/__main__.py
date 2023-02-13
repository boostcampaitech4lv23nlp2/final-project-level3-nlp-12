if __name__ =='__main__':
    import uvicorn
    uvicorn.run("local_main.main:app", host="0.0.0.0", port="", reload=True)