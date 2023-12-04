const FormatDate = (dateString) => {
  try {
      const date = new Date(dateString);
      if (isNaN(date)) {
          // Handle invalid date
          return "Invalid Date";
      }

      const options = {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
      };
      return new Intl.DateTimeFormat('en-US', options).format(date);
  } catch (error) {
      console.error("Error formatting date:", error);
      return "Invalid Date";
  }
};

export default FormatDate;
