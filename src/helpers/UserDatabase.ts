import {
	DynamoDBClient,
	GetItemCommand,
	PutItemCommand,
	UpdateItemCommand
} from '@aws-sdk/client-dynamodb';
import { unmarshall, marshall } from '@aws-sdk/util-dynamodb';
import { SECRET_AWS_SECRET, SECRET_AWS_KEY, SECRET_USER_TABLE } from '$env/static/private';
import type { UserProps } from '../types';

const clientOptions = {
	region: 'us-east-1',
	credentials: {
		accessKeyId: SECRET_AWS_KEY,
		secretAccessKey: SECRET_AWS_SECRET
	}
};

const client = new DynamoDBClient(clientOptions);

export const newUser = async (user: UserProps) => {
	await client.send(
		new PutItemCommand({
			TableName: SECRET_USER_TABLE,
			Item: marshall(user)
		})
	);
};

export const updateFavorites = async ({
	user_id,
	favorites
}: {
	user_id: string;
	favorites: string;
}) => {
	await client.send(
		new UpdateItemCommand({
			TableName: SECRET_USER_TABLE,
			Key: marshall({ user_id }),
			UpdateExpression: 'set favorites = :f',
			ExpressionAttributeValues: {
				':f': { S: favorites }
			}
		})
	);
};

export const getUser = async ({ user_id }: { user_id: string }): Promise<UserProps | null> => {
	const { Item } = await client.send(
		new GetItemCommand({
			TableName: SECRET_USER_TABLE,
			Key: marshall({ user_id })
		})
	);
	return Item ? (unmarshall(Item) as UserProps) : null;
};
