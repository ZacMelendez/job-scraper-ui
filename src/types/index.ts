export interface JobItemProps {
	company: string;
	job_id: string;
	title: string;
	jobUrl: string;
	location: string;
	type: 'job';
}

export interface JobSearchProps {
	must: string[];
	include: string[];
	exclude: string[];
	location: string[];
}

export interface UserProps {
	user_id: string;
	name: string;
	email: string;
	image: string;
	favorites: string | string[];
}
