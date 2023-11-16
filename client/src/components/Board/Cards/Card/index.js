import React from "react";
import styled from "styled-components";
import { Container, Draggable } from "react-smooth-dnd";
import { useEffect } from "react";
import { useState } from "react";
import { useMutation } from "@apollo/react-hooks";
import gql from "graphql-tag";

import { FaEdit, FaSave, FaBan, FaTrash } from "react-icons/fa";

const CardContainer = styled.div`
  display: flex;
  border-radius: 3px;
  border-bottom: 1px solid #ccc;
  background-color: #fff;
  position: relative;
  padding: 10px;
  cursor: pointer;
  max-width: 250px;
  margin-bottom: 7px;
  min-width: 230px;
`;

const SubmitCardIcon = styled.a`
  height: 32px;
  line-height: 32px;
  width: 32px;
`;

const CardContent = styled.div`
  width: 100%;
  justify-content: space-between;
  display: flex;
`;

const EditTitle = styled.input`
  width: 100%;
  margin-right: 3px;
  border: 1px dashed #80beff;
  :focus-visible {
    border: 1px dashed #80beff;
    outline: none;
  }
`;

const ActionContainer = styled.div`
  display: flex;
  width: 35px;
  justify-content: space-between;
`;
const UPDATE_CARD = gql`
  mutation UpdateCard($cardId: String!, $pos: Int!, $sectionId: String!, $title: String!, $label: String!) {
    updateCardData(
      cardEntry: { id: $cardId, pos: $pos, sectionId: $sectionId, title: $title, label: $label }
    ) {
      id
      title
      label
    }
  }
`;

const REMOVE_CARD = gql`
  mutation RemoveCard($cardId: String!) {
    deleteCardItem(
      cardEntry: { id: $cardId }
    ) {
      id
    }
  }
`;

const Card = ({ card, sectionId, setReload }) => {
  const [isEdit, setEdit] = useState(false);
  const [title, setTitle] = useState(card.title);

  const [updateCardPos, {data: updatedData }] = useMutation(UPDATE_CARD);
  const [removeCard, {data: removeRet }] = useMutation(REMOVE_CARD);

  useEffect(() => {
    if(updatedData != undefined) {
      setReload(Math.random());
    }
  }, [updatedData]);

  useEffect(() => {
    if(removeRet != undefined) {
      setReload(Math.random());
    }
  }, [removeRet]);

  const updateCard = () => {
    console.log(card, sectionId);
    if(title == '') {
      console.log('Title should not be empty');
      return;
    }
    // update mutation
    updateCardPos({
      variables: {
        cardId: card.id,
        pos: parseInt(card.pos),
        sectionId: sectionId,
        title: title,
        label: title,
      },
    });
    setEdit(false);
  };

  const deleteCard = () => {
    removeCard({
      variables: {
        cardId: card.id
      }
    })
  }

  return (
    <Draggable key={card.id}>
      <CardContainer className="card">
        {isEdit ? (
          <CardContent>
            <EditTitle 
            value={title}
            onChange={(e) => setTitle(e.target.value) }
            />
            <ActionContainer>
              <FaSave onClick={updateCard} />
              <FaBan onClick={()=> setEdit(false)} />
            </ActionContainer>
          </CardContent>
        ) : (
          <CardContent>
            {card.title}
            <ActionContainer>
            <FaEdit onClick={() => setEdit(true)} />
            <FaTrash style={{color: 'red'}} onClick={deleteCard}/>
            </ActionContainer>
          </CardContent>
        )}
      </CardContainer>
    </Draggable>
  );
};

export default Card;
