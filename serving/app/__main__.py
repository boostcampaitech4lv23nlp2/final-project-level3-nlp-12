if __name__ == '__main__':
    import uvicorn
    # uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=30001, reload=True)