import { z } from "zod";
import {
  createTRPCRouter,
  publicProcedure,
  protectedProcedure,
} from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity"
import { v1 as uuidv1 } from "uuid";
//importarDotenv

export const videoRouter = createTRPCRouter({
    uploadVideo: publicProcedure
      .input(z.object({ url: z.string() }))
      .query(({ input }) => {
        async function main() {
          try {
            
            //Conectarse con el servicio
            const AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING;

            if (!AZURE_STORAGE_CONNECTION_STRING) {
            throw Error('Azure Storage Connection string not found');
          }

            const blobServiceClient = BlobServiceClient.fromConnectionString(AZURE_STORAGE_CONNECTION_STRING);

            //Crear Container
            const containerName = 'urlVideos' + uuidv1();
            const containerClient = blobServiceClient.getContainerClient(containerName);
            const createContainerResponse = await containerClient.create();
            console.log(
              `Container was created successfully.\n\trequestId:${createContainerResponse.requestId}\n\tURL: ${containerClient.url}`
            );

            //Crear Blob
            const blobName = 'urlVideo' + uuidv1() + '.txt';
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);
            console.log(
              `\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`
            );

            //Upload Data
            const data = input.url;
            const uploadBlobResponse = await blockBlobClient.upload(data, data.length);
            console.log(
              `Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`
            );

        
          } catch (err: any) {
            console.log(`Error: ${err.message}`);
          }
        }
        
        main()
          .then(() => console.log("The video has been uploaded"))
          .catch((ex) => console.log(ex.message));
      }),
  });
  