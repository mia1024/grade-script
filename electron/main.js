// Modules to control application life and create native browser window
const { app, BrowserView, BrowserWindow, session } = require('electron')
const fs = require('fs')
const path = require('path')

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // and load the index.html of the app.
  const view = new BrowserView()
  mainWindow.loadFile('index.html')

  mainWindow.setBrowserView(view)
  view.setBounds({ x: 0, y: 0, width: 800, height: 600 })
  view.webContents.loadURL('https://www.gradescope.com/login')
  view.webContents.executeJavaScript("$('input[type=checkbox]').click()")
  view.webContents.on('page-title-updated',(e,title)=>{
    console.log(`In page ${title}`);
    if (title==='Your Courses | Gradescope'){
      console.log('Login Successful')
      mainWindow.close();
    }
  })

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()
  
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  app.quit()
  session.defaultSession.cookies.get({ url: 'https://www.gradescope.com' }).then(cookies=>{
    let toDump={}
    for (cookie of cookies){
      toDump[cookie.name]=cookie.value;
    }
    let s=JSON.stringify(toDump,null,4)
    fs.writeFileSync('cookies.json',s)
  })
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
