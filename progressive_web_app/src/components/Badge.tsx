import React from 'react';

type BadgeProps = {
    label: string;
};

const Badge:React.FC<BadgeProps> = ({label}) => {
    
    return <span  className='bg-primary/5 text-primary text-sm p-1 rounded-md font-semibold border border-primary/25'>{label}</span>
}
export default Badge;