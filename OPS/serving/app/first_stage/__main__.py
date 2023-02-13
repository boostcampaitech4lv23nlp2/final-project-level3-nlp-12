if __name__ == "__main__":
    import uvicorn

    uvicorn.run("first_stage.main:app", host="0.0.0.0", port="", reload=True)
