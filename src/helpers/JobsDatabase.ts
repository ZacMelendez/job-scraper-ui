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
	includeList?: string[];
	excludeList?: string[];
	companyList?: string[];
	exclusiveStartKey?: ExclusiveStartKey;
};

export async function queryTable(options: QueryTableOptions): Promise<JobItemProps[]> {
	const { includeList, excludeList, exclusiveStartKey, companyList } = options;

	if (exclusiveStartKey && (!('type' in exclusiveStartKey) || !('jobUrl' in exclusiveStartKey))) {
		throw new Error('Invalid exclusiveStartKey');
	}

	const filterExpressions = [''];

	if (includeList && includeList.length > 0) {
		const includeExpressions = includeList.map(
			(s) => `contains(#title, :${s.split(' ').join('_')})`
		);
		filterExpressions.push(`(${includeExpressions.join(' OR ')})`);
	}

	if (companyList && companyList.length > 0) {
		const companyExpressions = companyList.map(
			(s) => `contains(#company, :${s.split(' ').join('_')})`
		);
		filterExpressions.push(`(${companyExpressions.join(' OR ')})`);
	}

	if (excludeList && excludeList.length > 0) {
		const excludeExpressions = excludeList.map(
			(s) => `NOT contains(#title, :${s.split(' ').join('_')})`
		);
		filterExpressions.push(`(${excludeExpressions.join(' AND ')})`);
	}

	// console.log(filterExpressions.filter((expr) => !!expr).join(' AND '));

	const params: QueryCommandInput = {
		TableName: SECRET_JOBS_TABLE,
		KeyConditionExpression: '#type = :jobType',
		...((excludeList || includeList || companyList) && {
			FilterExpression: filterExpressions.filter((expr) => !!expr).join(' AND ')
		}),
		ExpressionAttributeNames: {
			'#type': 'type',
			...((includeList || excludeList) && { '#title': 'search_title' }),
			...(companyList && { '#company': 'company' })
		},
		ExpressionAttributeValues: {
			':jobType': { S: 'job' },
			...(excludeList
				? excludeList.reduce((acc, s) => ({ ...acc, [`:${s.split(' ').join('_')}`]: { S: s } }), {})
				: {}),
			...(includeList
				? includeList.reduce((acc, s) => ({ ...acc, [`:${s.split(' ').join('_')}`]: { S: s } }), {})
				: {}),
			...(companyList
				? companyList.reduce((acc, s) => ({ ...acc, [`:${s.split(' ').join('_')}`]: { S: s } }), {})
				: {})
		},
		...(!(includeList || excludeList) && { Limit: 20 }),
		ExclusiveStartKey: exclusiveStartKey
	};

	try {
		let data: QueryCommandOutput;
		let items: JobItemProps[];

		data = await client.send(new QueryCommand(params));
		items =
			data.Items?.map((item) => ({
				type: 'job',
				jobUrl: item.jobUrl.S || '',
				company: item.company.S || '',
				job_id: item.job_id.S || '',
				location: item.location.S || '',
				title: item.title.S || ''
			})) || [];

		while (items.length < 1) {
			const newCommand: QueryCommand = new QueryCommand({
				...params,
				ExclusiveStartKey: data?.LastEvaluatedKey
			});
			data = await client.send(newCommand);
			items =
				data.Items?.map((item) => ({
					type: 'job',
					jobUrl: item.jobUrl.S || '',
					company: item.company.S || '',
					job_id: item.job_id.S || '',
					location: item.location.S || '',
					title: item.title.S || ''
				})) || [];
		}

		return items;
	} catch (err) {
		console.error(err);
		return [];
	}
}
