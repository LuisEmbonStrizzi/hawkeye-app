import { z } from "zod";
import {
  createTRPCRouter,
  publicProcedure,
} from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";
import { env } from "~/env.mjs";
import axios from "axios";

export const videoRouter = createTRPCRouter({
    uploadVideo: publicProcedure
    .input(z.object({ video: z.string() }))
      .query(({ input }) => {
        async function main() {
          try {
            
            input = await axios.get("http://127.0.0.1:8000/getVideo", { responseType: 'text' });

            //Conectarse con el servicio

            if (!env.AZURE_STORAGE_CONNECTION_STRING) {
            throw Error('Azure Storage Connection string not found');
          }

            const blobServiceClient = BlobServiceClient.fromConnectionString(env.AZURE_STORAGE_CONNECTION_STRING);

            //Crear Container o elegir container preexistente
            const containerClient = blobServiceClient.getContainerClient("pruebavideos");

            //Crear Blob
            const blobName = 'Video' + uuidv1() + '.mp4';
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);
            console.log(
              `\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`
            );

            //Upload Data
            /*const response = await axios.get(input.video, { responseType: 'json' });
            const uploadBlobResponse = await blockBlobClient.upload(response.data, Buffer.byteLength(response.data));
            console.log(
              `Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`
            );*/

            //Prueba
            const response = await axios.get(input.video, { responseType: 'stream' });
            console.log(response)
            const uploadResponse = await blockBlobClient.uploadStream(response.data);
            console.log(
              `Blob was uploaded successfully. requestId: ${uploadResponse.requestId}`
            );
            const Video = {url: uploadResponse.requestId}
            return Video
        
          } catch (err: any) {
            console.log(`Error: ${err.message}`);
          }
        }
        
        main()
          .then(() => console.log("The video has been uploaded"))
          .catch((ex) => console.log(ex.message));
      }),
  });
  