import './MLScan.module.scss';
import React, { useState, useRef, useEffect, useContext, forwardRef, useCallback } from 'react';
import { useHistory, useParams } from 'react-router';
import updateProject from 'actions/project/update'
import { useReduxAction } from 'hooks/useReduxAction';
import Button from 'components/UI/Button/Button';
import { useRedux } from 'hooks/useRedux';
import { useTranslate } from 'hooks/useTranslate';
import { ProjectDetailsContext } from 'pages/Workspace/ProjectDetails/ProjectDetails';
import { NavLink } from 'react-router-dom';
import Webcam from 'react-webcam';

import indexActivity from 'actions/activity/index';
import Token from 'components/UI/Token/Token';
import ScanInfoModal from './components/ScanInfoModal';
import { motion, AnimatePresence } from 'framer-motion';

export default function MLScan() {

    const { theme, rootProject, handlePublication, setSaveKey } = useContext(
        ProjectDetailsContext
    );

    const translate = useTranslate();

    const userId = useRedux((state) => state.authentication?.user.id);

    const [isChecked, setIsChecked] = useState(!!rootProject?.is_public);

    const [randomToken, setRandomToken] = useState({});
    const [tokenInterval, setTokenInterval] = useState(0);
    const [isLoading, setIsLoading] = useState(false);
    const [emptyProject, setEmptyProject] = useState(false);
    const [showModal, setShowModal] = useState(true);
    const [notif, setNotif] = useState("");
    const [groowy, setGroowy] = useState({});
    const imageFile = useRef(null);
    const webcamRef = useRef(null);

    const dispatch = useReduxAction();

    useEffect(() => {
        dispatch(indexActivity());
    }, []);

    const { projectId } = useParams() as {
        projectId: string;
    };

    const history = useHistory();

    const activities = useRedux((state) => {
        const data = state.activity?.entities.allIds
            .map((id) => state.activity?.entities.byId[id])
            .filter((a) => a?.type === 'regular')
            // filter vrije activiteiten duplicates
            .filter(
                (value, i, arr) =>
                    arr.findIndex((activity) => activity?.name === value?.name) === i
            );
        
            if(projectId === "noTheme"){
                console.log("noTheme");
            }

        return data
    });

    const phases = useRedux((state) => {
        const data = state.phase?.entities.allIds.map(
            (id) => state.phase?.entities.byId[id]
        );

        return data
    });

    function dataURLtoBlob(dataurl) {
        if (!dataurl) return;

        const arr = dataurl.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
    }

    function notification(text) {
        setNotif(text);

        setTimeout(() => {
            setNotif('');
        }, 5000);
    }

    const videoConstraints = {
        width: 1920,
        height: 1080,
        facingMode: "environment"
    };

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        onFileUpload(imageSrc);
        setRandomToken(getRandomToken());
    }, [webcamRef]);

    const getRandomToken = () => {
        const tokenLength = activities?.length - 2;
        const randomIndex = parseInt(Math.random() * tokenLength) + 1;
        let token = activities?.find((activity) => activity.id === randomIndex);
        console.log(token?.slug);
        if (!token?.slug) token = activities?.find((activity) => activity.slug === 'groowy');
        return token;
    }

    const findToken = (slug) => {
        let token = activities?.find((activity) => activity.slug === slug);

        if (!token) {
            token = phases?.find((phase) => phase.slug === slug);
        }

        return token;
    };

    useEffect(() => {
        const groowyToken = findToken('groowy');
        setGroowy(groowyToken);
    }, []);


    const onFileUpload = (imageSrc) => {
        setIsLoading(true);

        const tokenInterval = setInterval(() => {
            setRandomToken(getRandomToken());
        }, 600);
        setTokenInterval(tokenInterval);

        const ImageURL = imageSrc;
        const blob = dataURLtoBlob(ImageURL);

        console.log(imageSrc);

        dispatch(updateProject({
            processMlImage: true,
            id: projectId,
            image: blob,
        }))
            .then((project) => {
                console.log(project);
                clearInterval(tokenInterval);
                setIsLoading(false);
                if (project.process.length == 0) {
                    console.log("empty project");
                    setEmptyProject(true);
                    notification(`${translate('scan.error.process-not-recognized')}`);
                } else {
                    // dispatch(indexProject()).then(() => setSaveKey(prev => prev+1));
                    history.push(`/werkplaats/project-details/${project.id}`);
                }

            })
            .catch(() => {
                clearInterval(tokenInterval);
                setIsLoading(false);
                notification(`${translate('scan.error.process-not-recognized')}`);
            });

    };

    return (
        <div styleName="scanner">
            <div styleName="click-field" onClick={capture} />
            {notif && (
                <div styleName="notification-container">
                    <div
                        styleName="groowy"
                        style={{ backgroundImage: `url(${groowy && groowy.thumbnail})` }}
                    />
                    <div styleName="notifications">
                        {`"${notif}"`} 
                    </div>
                </div>
            )}
            <div styleName="frame">
                <div styleName='tokens'>
                    {randomToken && 'thumbnail' in randomToken && isLoading && <Token token={randomToken} />}
                </div>
                <svg
                    version="1.0"
                    id="Layer_1"
                    xmlns="http://www.w3.org/2000/svg"
                    x="0px"
                    y="0px"
                >
                    <g>
                        <path
                            fill="none"
                            stroke="#FFFFFF"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeMiterlimit="10"
                            d="M225.5,33.8V9.36
c0-3.79-3.07-6.86-6.86-6.86H194.2"
                            transform='translate(1495, 0)'
                        />
                        <path
                            fill="none"
                            stroke="#FFFFFF"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeMiterlimit="10"
                            d="M2.5,194.2v24.44
c0,3.79,3.07,6.86,6.86,6.86H33.8"
                            transform='translate(0, 740)'
                        />
                        <path
                            fill="none"
                            stroke="#FFFFFF"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeMiterlimit="10"
                            d="M33.8,2.5H9.36
C5.57,2.5,2.5,5.57,2.5,9.36V33.8"
                            transform='translate(0, 0)'
                        />
                        <path
                            fill="none"
                            stroke="#FFFFFF"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeMiterlimit="10"
                            d="M194.2,225.5h24.44
c3.79,0,6.86-3.07,6.86-6.86V194.2"
                            transform='translate(1495, 740)'
                        />
                    </g>
                </svg>
                {/* <AnimatePresence>
                    {(isLoading) && (
                        <motion.img
                            key={randomToken?.thumbnail}
                            src={randomToken?.thumbnail}
                            transition={{duration:0.5}}
                            initial={{ opacity: 0.5, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0.5, scale: 0.5 }}
                            onAnimationComplete={() => setRandomToken(getRandomToken())}
                        />
                    )}
                </AnimatePresence> */}
            </div>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
            />
            <AnimatePresence>
                {showModal && (
                    <ScanInfoModal setModalIsOpen={setShowModal} />
                )}
            </AnimatePresence>
        </div>
    );
}
