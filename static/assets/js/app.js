ValidateView.post('/validate', async (request, response) => {
    const file = request.files.photo;
    const s3 = new AWS.S3({
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    });
    const params = {
      Bucket: process.env.AWS_BUCKET_NAME,
      Key: file.name,
      Body: fs.createReadStream(file.path)
    };
    s3.upload(params, async (error, data) => {
      if (error) {
        response.status(500).send(error);
      } else {
        const paramsSageMaker = {
          EndpointName: 'YourSageMakerEndpoint', // cambiar por nombre del endpoint de SageMaker
          Body: fs.createReadStream(file.path),
          ContentType: 'application/x-image',
        };
        const result = await sagemakerRuntime.invokeEndpoint(paramsSageMaker).promise();
        const prediction = JSON.parse(result.Body.toString()); // Suponiendo que el resultado es un objeto JSON
        response.status(200).send(`El árbol frutal reconocido es ${prediction.fruitTreeType} con un porcentaje de aprobación de ${prediction.approvalPercentage}%`);
      }
    });
  });