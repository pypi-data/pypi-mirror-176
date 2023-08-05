import os
import uvicorn
from uvicorn import Server

def run(user_filename='main'):
    uvicorn.run(
        f"{user_filename}:hs",
        host="127.0.0.1",
        port=8083,
        reload="True",
        factory=True,
        app_dir=os.getcwd(),
        reload_dirs=[os.getcwd()],
    )


if __name__ == "__main__":
    run()