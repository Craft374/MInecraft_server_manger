const { app, BrowserWindow } = require('electron');
const path = require('path');

/** 메인 창 생성 */
function createWindow () { 
  let win = new BrowserWindow({
    width: 1900,
    height: 9720,
    webPreferences: { preload: path.join(__dirname, 'preload.js') } //path.join()으로 전처리 url 또는 file을 설정할 수 있음
  })
  console.log(win.getBounds());

  //브라우저창이 읽어 올 파일 위치
  win.loadFile('./index.html')
}

/** Application이 준비된 후 실행할 스크립트를 지정*/
app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
