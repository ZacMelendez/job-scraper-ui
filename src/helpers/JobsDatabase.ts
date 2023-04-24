import {
	DynamoDBClient,
	QueryCommand,
	type QueryCommandOutput,
	type QueryCommandInput
} from '@aws-sdk/client-dynamodb';
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

type ExclusiveStartKey = QueryCommandInput['ExclusiveStartKey'];

type QueryTableOptions = {
	search?: string;
	excludeList?: string[];
	exclusiveStartKey?: ExclusiveStartKey;
};

export async function queryTable(options: QueryTableOptions): Promise<JobItemProps[]> {
	const { search, excludeList, exclusiveStartKey } = options;

	if (exclusiveStartKey && (!('type' in exclusiveStartKey) || !('jobUrl' in exclusiveStartKey))) {
		throw new Error('Invalid exclusiveStartKey');
	}

	const filterExpressions = [
		search
			? `(contains(#company, :search) OR contains(#location, :search) OR contains(#title, :search))`
			: ''
	];

	if (excludeList && excludeList.length > 0) {
		const excludeExpressions = excludeList.map((s) => `NOT contains(#title, :${s})`);
		filterExpressions.push(`(${excludeExpressions.join(' AND ')})`);
	}

	const params: QueryCommandInput = {
		TableName: SECRET_JOBS_TABLE,
		KeyConditionExpression: '#type = :jobType',
		...((excludeList || search) && {
			FilterExpression: filterExpressions.filter((expr) => !!expr).join(' AND ')
		}),
		ExpressionAttributeNames: {
			'#type': 'type',
			...((search || excludeList) && { '#title': 'title' }),
			...(search && { '#company': 'company', '#location': 'location' })
		},
		ExpressionAttributeValues: {
			':jobType': { S: 'job' },
			...(excludeList ? excludeList.reduce((acc, s) => ({ ...acc, [`:${s}`]: { S: s } }), {}) : {}),
			...(search ? { ':search': { S: search } } : {})
		},
		...(!search && { Limit: 20 }),
		ExclusiveStartKey: exclusiveStartKey
	};

	try {
		const data: QueryCommandOutput = await client.send(new QueryCommand(params));
		const items: JobItemProps[] =
			data.Items?.map((item) => ({
				type: 'job',
				jobUrl: item.jobUrl.S || '',
				company: item.company.S || '',
				job_id: item.job_id.S || '',
				location: item.location.S || '',
				title: item.title.S || ''
			})) || [];

		return items;
	} catch (err) {
		console.error(err);
		return [];
	}
}
