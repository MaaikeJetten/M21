// Components==============
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useMediaQ } from 'hooks/useMediaQ';
import { usePermission } from 'hooks/usePermission';
import { useTranslate } from 'hooks/useTranslate';
import { useRedux } from 'hooks/useRedux';
import React, { useContext, useEffect, useState, useRef } from 'react';
import { PageType } from 'typings';
import { getNoContentItems } from 'utilities/getNoContentItems';
import { GlobalBuildingBlocksMountedContext } from 'utilities/GlobalContext/GlobalBuildingBlocksMounted';
import Button from '../Button/Button';
import RichText from '../RichText/RichText';
import Spinner from '../Spinner/Spinner';
import './NoContent.module.scss';
import { useReduxAction } from 'hooks/useReduxAction';
import updateProject from 'actions/project/update';
import { useHistory } from 'react-router';
import Token from 'components/UI/Token/Token';
import indexActivity from 'actions/activity/index';
import StartPoint from '../ProjectProcess/components/StartPoint/StartPoint';
// =========================

export default function NoContent({
  page,
  loading,
  hasContent,
  isTeacherMember,
  children,
  loadOnce,
  decreasedHeight,
  handleClick,
  sharecode,
  marginTop,
  returnNothing = false,
  project_id,
}: {
  page: PageType;
  loading: boolean;
  hasContent: boolean;
  isTeacherMember?: boolean;
  children: React.ReactNode;
  loadOnce?: boolean;
  decreasedHeight?: 50 | 70;
  handleClick?: () => void;
  sharecode?: React.ReactNode;
  marginTop?: string;
  returnNothing?: boolean;
  project_id?: number;
}) {
  const translate = useTranslate();
  const { img, title, description, buttons, conditions } = getNoContentItems(
    page,
    translate
  );

  const { buildingBlocksMounted, setBuildingBlocksMounted } = useContext(
    GlobalBuildingBlocksMountedContext
  );

  const [selectedFile, setSelectedFile] = useState(null);
  const [scanLoading, setScanLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);
  const [randomToken, setRandomToken] = useState({});
  const [tokenInterval, setTokenInterval] = useState(0);
  const [largeFile, setLargeFile] = useState(false);
  const [emptyProject, setEmptyProject] = useState(false);
  const hiddenFileInput = useRef(null);

  const dispatch = useReduxAction();
  const history = useHistory();

  const handleScan = event => {
    hiddenFileInput.current.click();
    setEmptyProject(false);
  }

  useEffect(() => {
    dispatch(indexActivity());
  }, []);

  const activities = useRedux((state) => {
      const data = state.activity?.entities.allIds
        .map((id) => state.activity?.entities.byId[id])
        .filter((a) => a?.type === 'regular')
        // filter vrije activiteiten duplicates
        .filter(
          (value, i, arr) =>
            arr.findIndex((activity) => activity?.name === value?.name) === i
        );

    return data
  });

  const getRandomToken = () => {
    const tokenLength = activities?.length - 5;
    const randomIndex = parseInt(Math.random() * tokenLength) + 1;
    let token = activities?.find((activity) => activity.id === randomIndex);
    return token;
  }

  const onFileChange = (event) => {

    // Update the state
    const file = event.target.files[0];
    setSelectedFile(file);
    console.log(file);
    setRandomToken(getRandomToken());

    if (event.target.files[0].size > 5000000) {
      setLargeFile(true);
    } else {
      setLargeFile(false);
      onFileUpload(file);
    }

  };

  const onFileUpload = (file) => {
    // console.log(file);
    setScanLoading(true);

    const tokenInterval = setInterval(() => {
      setRandomToken(getRandomToken());
    }, 500);
    setTokenInterval(tokenInterval);

    dispatch(updateProject({
      processMlImage: true,
      image: file,
      id: project_id,
    }))
      .then((project) => {
        // console.log(project);
        clearInterval(tokenInterval);
        setScanLoading(false);
        if (project.process.length == 0) {
          console.log("empty project");
          setEmptyProject(true);
        } else {
          // dispatch(indexProject()).then(() => setSaveKey(prev => prev + 1));
          history.push(`/werkplaats/project-details/${project.id}`);
        }
      })

  };

  useEffect(() => {
    if (loadOnce && !buildingBlocksMounted) {
      const timeout = setTimeout(() => {
        setBuildingBlocksMounted(true);
      }, 3000);

      return () => clearTimeout(timeout);
    }
  }, []);

  const query = useMediaQ('min', 1024);
 
  if (scanLoading && !hasContent)
    return (
      <div
        styleName="nocontent"
        style={{
          height: decreasedHeight ? `${decreasedHeight}%` : '',
          marginTop,
        }}
      >
        <div styleName="content-wrapper">
          <div styleName='token'>
          {randomToken && 'thumbnail' in randomToken && <Token token={randomToken} />}
            <h3>{translate('project.actions.scanning')}</h3>
          </div>
        </div>
      </div>
    );

  return (
    <div
      styleName="nocontent"
      style={{
        height: decreasedHeight ? `${decreasedHeight}%` : '',
        marginTop,
      }}
    >
      <div styleName="content-wrapper">
        <div styleName="image-wrapper">
          <img alt={page} src={`/images/error-illustrations/${img}.svg`} />
        </div>
        {!(conditions?.includes('teacher') && !isTeacher) && (
          <>
            <h1>{title}</h1>
            <div styleName="rich-text">
              <RichText content={description} />
            </div>
            {buttons && (
              <div styleName="buttons-wrapper">
                {buttons.map((button, index) => {
                  if (button.conditions?.includes('scan'))
                    return (
                      <>
                        <Button
                          key={index}
                          to={button.to ? button.to : undefined}
                          onClick={handleScan}
                        >
                          {button.name}
                          {button.icon && <FontAwesomeIcon icon={button.icon} />}
                        </Button>
                        <input key= {index+1} type="file" ref={hiddenFileInput} onChange={onFileChange} />
                        {/* <Button
                          key={index+2}
                          to={`/mlscan/${project_id}`}
                          onClick={handleClick}
                          >
                            {translate('project.actions.add-scan-process')}
                          </Button> */}
                      </>
                    )

                  return (
                    <Button
                      key={index}
                      to={button.to ? button.to : undefined}
                      onClick={!button.to ? handleClick : undefined}
                    >
                      {button.name}
                      {button.icon && <FontAwesomeIcon icon={button.icon} />}
                    </Button>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
