
import { useEffect } from 'react';
import { useStoreState, useStoreActions } from 'easy-peasy';


import './StatusMessage.css'



const StatusMessage = () => {
  const errMsg = useStoreState((state) => state.errMsg)
  const setErrMsg = useStoreActions((actions) => actions.setErrMsg)
  
  const infoMsg = useStoreState((state) => state.infoMsg)
  const setInfoMsg = useStoreActions((actions) => actions.setInfoMsg)

  // clear infoMsg after 4 seconds
  useEffect(() => {
    if (infoMsg) {
      const timeoutId = setTimeout(() => {
        setInfoMsg('');
      }, 4000);
      return () => clearTimeout(timeoutId);
    }
  }, [infoMsg, setInfoMsg]);
  useEffect(() => {
    if (errMsg) {
      const timeoutId = setTimeout(() => {
        setErrMsg('');
      }, 60000);
      return () => clearTimeout(timeoutId);
    }
  }, [errMsg, setErrMsg]);

  return (
    <>
        { errMsg && <div className='errmsg' aria-live="assertive">{errMsg}</div>}
        { infoMsg && <div className='ingomsg' aria-live="assertive">{infoMsg}</div>}
    </>
  )
}

export default StatusMessage