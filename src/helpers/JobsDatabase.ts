import { DynamoDBClient, ScanCommand, QueryCommand } from '@aws-sdk/client-dynamodb';
import { unmarshall } from '@aws-sdk/util-dynamodb';
import { SECRET_AWS_SECRET, SECRET_AWS_KEY, SECRET_JOBS_TABLE } from '$env/static/private';
import type { JobItemProps } from '../types';

const clientOptions = {
	region: 'us-east-1',
	credentials: {
		accessKeyId: SECRET_AWS_KEY,
		secretAccessKey: SECRET_AWS_SECRET
	}
};

// import AmazonDaxClient from 'amazon-dax-client';
// import AWS from 'aws-sdk';

// import { DAXClient, CreateClusterCommand } from "@aws-sdk/client-dax";

// // Replace this ...
// const ddb = new AWS.DynamoDB(clientOptions);
// /// with this ...
// const endpoint = 'daxs://job-scraper-jobs.cbszpm.dax-clusters.us-east-1.amazonaws.com';
// const dax = new AmazonDaxClient({ endpoints: [endpoint], region: 'us-east-1' });

// // If using AWS.DynamoDB.DocumentClient ...
// const doc = new AWS.DynamoDB.DocumentClient({ service: dax });

const client = new DynamoDBClient(clientOptions);

export const getJobs = async ({
	lastEvalKey,
	search
}: {
	lastEvalKey?: string;
	search?: string;
}): Promise<JobItemProps[]> => {
	try {
		const command = new ScanCommand({
			TableName: SECRET_JOBS_TABLE,
			Limit: 20,
			...(lastEvalKey && {
				ExclusiveStartKey: {
					jobUrl: {
						S: lastEvalKey
					}
				}
			}),
			...(search && {
				FilterExpression: 'contains(title, :search) or contains(location, :search)',
				ExpressionAttributeValues: { ':search': { S: search } }
			}),
			ReturnConsumedCapacity: 'TOTAL'
		});

		const Items = await client.send(command);

		search && console.log(Items?.Items);

		const posts = Items?.Items?.map((item) => unmarshall(item));
		return posts as JobItemProps[];
	} catch (err) {
		console.error(err);
		return [];
	}
};
