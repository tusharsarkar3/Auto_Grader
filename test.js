const fs = require('fs');
const request = require('request');

    const options = {
      method: 'POST',
      url: 'https://pen-to-print-handwriting-ocr.p.rapidapi.com/recognize/',
      headers: {
        'content-type': 'multipart/form-data; boundary=---011000010111000001101001',
        "x-rapidapi-key": "915f758cb5mshbb558a904c64455p14aa0ajsnec22ba2f1c80",
        'x-rapidapi-host': 'pen-to-print-handwriting-ocr.p.rapidapi.com',
        useQueryString: true
      },
      formData: {
        srcImg: {
          value: fs.createReadStream('page1.jpg'),
          options: {filename: 'page1.jpg', contentType: 'application/octet-stream'}
        },
        Session: 'string'
      }
    };

    request(options, function (error, response, body) {
        if (error) throw new Error(error);

        console.log(body);
        fs.writeFile('output.txt', body, (err) => {

        // In case of a error throw err.
        if (err) throw err;
    })

        return body
    });
