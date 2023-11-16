import React, { useState, useEffect } from "react";
import CardContainer from "./Cards/CardsContainer";
import { Container } from "react-smooth-dnd";
import { IoIosAdd } from "react-icons/io";
import sortBy from "lodash/sortBy";
import { useMutation, useSubscription, useQuery, useLazyQuery } from "@apollo/react-hooks";

import gql from "graphql-tag";
import PosCalculation from "../../utils/pos_calculation";
import {
  BoardContainer,
  CardHorizontalContainer,
  AddSectionDiv,
  AddSectionForm,
  AddSectionLink,
  AddSectionLinkSpan,
  AddSectionLinkIconSpan,
  AddSectionInput,
  ActiveAddSectionInput,
  SubmitCardButtonDiv,
  SubmitCardButton,
  SubmitCardIcon,
} from "./board.styles";

const BOARD_QUERY = gql`
  query {
    allSectionData {
      sectionInfo
    }
  }
`;

const BOARD_SUBSCRIPTION = gql`
  subscription {
    sectionAdded {
      id
      title
      label
      description
      pos
      cards {
        id
        title
        label
        pos
        description
      }
    }
  }
`;

const ADD_SECTION = gql`
  mutation AddSection($title: String!, $label: String!, $pos: Int!) {
    sectionData(sectionEntry: { title: $title, label: $label, pos: $pos }) {
      title
      label
      pos
    }
  }
`;

const UPDATE_SECTION_POS = gql`
  mutation UpdateSection($sectionId: String!, $pos: Int!, $title: String!, $label: String!) {
    updateSectionData(sectionEntry: { id: $sectionId, pos: $pos, title: $title, label: $label }) {
      id
    }
  }
`;

const ON_SECTION_POS_CHANGES = gql`
  subscription {
    onSectionPosChange {
      id
      pos
    }
  }
`;

// const REORDER_SECTION = gql``;

const Board = () => {
  const [reload , setReload] = useState();
  const [isAddSectionInputActive, setAddSectionInputActive] = useState(false);

  const [addSectionInpuText, setAddSectionInputText] = useState("");
  const [boards, setBoards] = useState([]);

  const [AddSection, { data: {sectionData} ={}  } ] = useMutation(ADD_SECTION);

  // const [getBoardData, { error, data, refetch }] = useQuery(BOARD_QUERY);
  const { loading, error, data, refetch } = useQuery(BOARD_QUERY);

  const [updateSectionPos, {data: dataUSP }] = useMutation(UPDATE_SECTION_POS);

  useEffect(()=> {
    refetch();
  }, []);

  useEffect(() => {
    if (data) {
      const _data = JSON.parse(data.allSectionData.sectionInfo);
      let tmp = [];
      _data.forEach(element => {
        let cardsTmp = [];
        let _tmpCard = element.cards;
        _tmpCard.forEach(element2 => {
          const _id = element2.id.S;
          const _title = element2.title.S;
          const _label = element2.label.S;
          const _sectionId = element2.sectionId.S;
          const _pos = element2.pos.N;
          element2.id = _id;
          element2.title = _title;
          element2.label = _label;
          element2.pos = _pos;
          element2.sectionId = _sectionId;
          cardsTmp.push(element2);
        });

        const _id = element.id.S;
        const _pos = element.pos.N;
        const _title = element.title.S;
        const _label = element.label.S;
        element.id = _id;
        element.pos = _pos;
        element.title = _title;
        element.label = _label;
        element.cards = cardsTmp;
        tmp.push(element);
      });
      console.log(tmp);
      setBoards(tmp);
    }
  }, [data]);

  useEffect(() => {
    if(sectionData != undefined) {
      refetch();
    }
  }, [ sectionData ]);

  useEffect(() => {
    if(dataUSP != undefined) {
      refetch();
    }
  }, [ dataUSP]);

  useEffect(() => {
    if(reload != undefined) {
      refetch();
    }
  }, [reload]);

  const { data: { sectionAdded } = {} } = useSubscription(BOARD_SUBSCRIPTION);

  const { data: { onSectionPosChange } = {} } = useSubscription(
    ON_SECTION_POS_CHANGES
  );

  useEffect(() => {
    if (onSectionPosChange) {
      console.log("onSectionPosChange", onSectionPosChange);
      let newBoards = boards;

      newBoards = newBoards.map((board) => {
        if (board.id === onSectionPosChange.id) {
          return { ...board, pos: onSectionPosChange.pos };
        } else {
          return board;
        }
      });
      let sortedBoards = sortBy(newBoards, [
        (board) => {
          return board.pos;
        },
      ]);
      console.log("useEffect", sortedBoards);
      setBoards(sortedBoards);
    }
  }, [onSectionPosChange]);

  useEffect(() => {
    if (sectionAdded) {
      setBoards(boards.concat(sectionAdded));
    }
  }, [sectionAdded]);

  const onColumnDrop = ({ removedIndex, addedIndex, payload }) => {
    if (boards) {
      console.log(boards);
      let updatePOS = PosCalculation(
        removedIndex,
        addedIndex,
        boards
      );
      let newBoards = boards.map((board) => {
        if (board.id === payload.id) {
          return { ...board, pos: updatePOS };
        } else {
          return board;
        }
      });

      let sortedBoards = sortBy(newBoards, [
        (board) => {
          return board.pos;
        },
      ]);

      updateSectionPos({
        variables: {
          sectionId: payload.id,
          pos: parseInt(updatePOS),
          title: payload.title,
          label: payload.label,
        },
      });
      // setBoards([...sortedBoards]);
    }
  };

  const onAddSectionSubmit = () => {
    if (addSectionInpuText) {
      AddSection({
        variables: {
          title: addSectionInpuText,
          label: addSectionInpuText,
          pos:
            boards && boards.length > 0
              ? parseInt(boards[boards.length - 1].pos) + 16384
              : 16384,
        },
      });
      setAddSectionInputText('');
    }
  };

  return (
    <BoardContainer>
      <Container
        orientation={"horizontal"}
        onDrop={onColumnDrop}
        onDragStart={() => {
          console.log("on drag start");
        }}
        getChildPayload={(index) => {
          return boards[index];
        }}
        dragHandleSelector=".column-drag-handle"
        dropPlaceholder={{
          animationDuration: 150,
          showOnTop: true,
          className: "cards-drop-preview",
        }}
      >
        {boards.length > 0 &&
          boards.map((item, index) => (
            <CardContainer item={item} key={index} boards={boards} setReload={setReload}/>
          ))}
      </Container>
      <AddSectionDiv onClick={() => setAddSectionInputActive(true)}>
        <AddSectionForm>
          {isAddSectionInputActive ? (
            <React.Fragment>
              <ActiveAddSectionInput
                value={addSectionInpuText}
                onChange={(e) => setAddSectionInputText(e.target.value)}
              />
              <SubmitCardButtonDiv>
                <SubmitCardButton
                  type="button"
                  value="Add Card"
                  onClick={onAddSectionSubmit}
                />
                <SubmitCardIcon>
                  <IoIosAdd />
                </SubmitCardIcon>
              </SubmitCardButtonDiv>
            </React.Fragment>
          ) : (
            <React.Fragment>
              <AddSectionLink href="#">
                <AddSectionLinkSpan>
                  <IoIosAdd size={28} />
                  Add another list
                </AddSectionLinkSpan>
              </AddSectionLink>
              <AddSectionInput />
            </React.Fragment>
          )}
        </AddSectionForm>
      </AddSectionDiv>
    </BoardContainer>
  );
};

export default Board;
