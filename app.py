from vibora import Vibora
from vibora.static import StaticHandler

import time

app = Vibora(
    template_dirs=['.'],
    static=StaticHandler([
        './static',
    ])
)

@app.route('/')
async def home():
    image = [
        'https://blobscdn.gitbook.com/v0/b/gitbook-28427.appspot.com/o/spaces%2F-LBXE_KGkYB72zVSpU-1%2Favatar.png?generation=1525478070771821&alt=media',
    ]

    print('home is runnning')
    print('append new image')
    image.append(
        'https://i.pinimg.com/originals/c6/d4/d5/c6d4d5325e2c8e3a5b47531b1c4db4ff.gif'
    )
    time.sleep(1)
    print('image has appended')
    return await app.render('index.html', images=image)

if __name__ == '__main__':
    app.run(debug=True, workers=6, host='0.0.0.0', port=8080)
