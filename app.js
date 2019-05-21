var express = require('express')
var app = express()
var multer  = require('multer')
var bodyParser    = require('body-parser');
var cors          = require("cors");
const path = require("path");
const fs = require("fs");
const { exec } = require('child_process');
const moment = require('moment');


const handleError = (err, res) => {
  res
    .status(500)
    .contentType("text/plain")
    .end("Oops! Something went wrong!");
};

const upload = multer({
  dest: "files"
  // you might also want to set some limits: https://github.com/expressjs/multer#limits
});

app.use(cors());
app.use(bodyParser.json());

// app.get('/teste', (req, res) => {
// res.send(200, {})        
// })   


app.get(
  "/teste?", (req, res) => {

    console.log(req)
let str = req.originalUrl;
    var obj = {}; 
   str = str.replace('/teste?', "")
str.replace(/([^=&]+)=([^&]*)/g, function(m, key, value) {
    obj[decodeURIComponent(key)] = decodeURIComponent(value);
}); 	

console.log(`R CMD BATCH --no-save --no-restore '--args  values=c(${obj.values})' /home/tradersclub/tcc/test.R`)

    exec(`R CMD BATCH --no-save --no-restore '--args  values=c(${obj.values})' ~/tcc/test.R`, (err, stdout, stderr) => {
      if (err) {
        // node couldn't execute the command
        return;
      }
    
      // the *entire* stdout and stderr (buffered)
      console.log(`stdout: ${stdout}`);
      console.log(`stderr: ${stderr}`);
    });
  res
    .status(200)
    .contentType("text/plain")
    .end("File uploaded!");
});
    // res.send(200)

app.post(
  "/upload",
  upload.single("file" /* name attribute of <file> element in your form */),
  (req, res) => {
    const tempPath = req.file.path;
    const body = req.body;
    let date = moment(new Date()).format('MMMM-DD-YYYY-hh-mm-ss'); 
    const targetPath = path.join( `files/${date}` );

 //   if (path.extname(req.file.originalname).toLowerCase() === ".jpg") {
      fs.rename(tempPath, targetPath, err => {
        if (err) return handleError(err, res);
        exec(`convert ${targetPath} -resize 96x96\! ${targetPath}_96x96.png` );
        exec(`python3 test_classify.py -i ${targetPath}_96x96.png`, (err, stdout, stderr) => {
            if (err) {
              console.log(`err: ${err}`);
              return;
            }
          
            // the *entire* stdout and stderr (buffered)
            console.log(`stdout: ${stdout}`);
            console.log(`stderr: ${stderr}`);
            res
              .status(200)
              .contentType("text/plain")
              .end(`File uploaded! \n${stdout}`);

          });
      });
    // } else {    
    //   fs.unlink(tempPath, err => {
    //     if (err) return handleError(err, res);

    //     res
    //       .status(403)
    //       .contentType("text/plain")
    //       .end("Only .jpg files are allowed!");
    //   });
    // }
  }
);

app.listen(3333)
console.log("Listening on localhost:3333")