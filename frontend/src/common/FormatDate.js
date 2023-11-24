const FormatDate = (dateString) => {
    const date = new Date(dateString);
    const options = {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      };
    return new Intl.DateTimeFormat('en-US', options).format(date);
  };

export default FormatDate
