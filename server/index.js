const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const req = require('express/lib/request');
const res = require('express/lib/response');

const port = 5000;

const app = express();

app.use(cors());

const uploads = multer({
    dest: __dirname + "/uploads",
});

app.post("/uploads", uploads.single("image"), (req, res) => {
    const spawn = require('child_process').spawn;
    var process = spawn('python', ['./preprocessing/predict.py', req.file.path]);
    var scriptData = "";
    var errorData = "";

    process.stdout.on('data', function(data){
        scriptData = data.toString().replace(/(\r\n|\n|\r)/gm,""); ;
        console.log(scriptData);
    });

    process.stderr.on('data', (data) => {
        errorData = data.toString().replace(/(\r\n|\n|\r)/gm, '');
        console.error(errorData);
    });

    process.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        const resp = {
            status: "file received and processed",
            class: scriptData,
        };
        res.json(resp);
    })
});

app.listen(port, function(){
    console.log("Server running on port 5000");
})