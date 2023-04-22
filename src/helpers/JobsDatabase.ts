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

const client = new DynamoDBClient(clientOptions);

export const getJobs = async ({
	lastEvalKey,
	search
}: {
	lastEvalKey?: string;
	search?: string;
}): Promise<JobItemProps[]> => {
	try {
		const command = search
			? new QueryCommand({
					TableName: SECRET_JOBS_TABLE,
					...(lastEvalKey && {
						ExclusiveStartKey: {
							jobUrl: {
								S: lastEvalKey
							}
						}
					}),
					Limit: 20,
					...(search && {
						KeyConditionExpression: '#jobType = :type',
						FilterExpression: 'contains(#jobTitle, :search) OR contains(#jobLocation, :search)',
						ExpressionAttributeValues: { ':search': { S: search }, ':type': { S: 'job' } },
						ExpressionAttributeNames: {
							'#jobType': 'type',
							'#jobLocation': 'location',
							'#jobTitle': 'title'
						}
					}),
					ReturnConsumedCapacity: 'TOTAL'
			  })
			: new ScanCommand({
					TableName: SECRET_JOBS_TABLE,
					...(lastEvalKey && {
						ExclusiveStartKey: {
							jobUrl: {
								S: lastEvalKey
							},
							type: {
								S: 'job'
							}
						}
					}),
					ReturnConsumedCapacity: 'TOTAL',
					Limit: 20
			  });

		const Items = await client.send(command);

		const posts = Items?.Items?.map((item) => unmarshall(item));
		return posts as JobItemProps[];
	} catch (err) {
		console.error(err);
		return [];
	}
};
