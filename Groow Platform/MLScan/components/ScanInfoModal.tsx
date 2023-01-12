import Modal from 'components/UI/Modal/Modal';
import Button from 'components/UI/Button/Button';
import { useTranslate } from 'hooks/useTranslate';
import React from 'react';

import './ScanInfoModal.module.scss';

export default function ScanModal({
  setModalIsOpen,
}: {
  setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {

  const translate = useTranslate();

  function handleClick() {
    setModalIsOpen(false);
  }

  return (
    <Modal setModalIsOpen={setModalIsOpen} size="medium">
      <div styleName="modalContent2">
        <div styleName="image-wrapper">
          <img src="/images/Scannen.svg" alt="scannen" />
        </div>
        <h1>{translate('scan.modal.label')}</h1>
        <div styleName='description'>
          <p>
            {translate('scan.modal.description')}
            <br /> <br />
            {translate('scan.modal.point-1')}
            <br />
            {translate('scan.modal.point-2')}
            <br />
            {translate('scan.modal.point-3')}
            <br />
            {translate('scan.modal.point-4')}
            <br /> <br />
            {translate('scan.modal.description-2')}
          </p>
        </div>

        <div styleName="buttons-wrapper">
          <Button
            onClick={handleClick}
          >
            {translate('scan.modal.button')}
          </Button>
        </div>
      </div>
    </Modal>
  );
}