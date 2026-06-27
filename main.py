from fastapi import FastAPI, HTTPException  # fastapi 라는 패키지에서 FastAPI 라는 클래스를 가져옴
from models import board
from models.item import Item # models 폴더 내부의 item.py 파일로부터 Item 클래스를 가져온다
from routers.boardRouters import router as board_router
app = FastAPI() # FastAPI 인스턴스 생성
app.include_router(board_router)
# / 경로
# 웹 사이트에 가장 첫 페이지(메인페이지)를 뜻함 한마디로 루트경로
# 브라우저에 naver.com을 치고 엔터하면 실제로 뒤에 슬래시가 생략된
# naver.com/ 으로 접속하는 것임
@app.get("/")
async def hello():
    return {"message": "Hello World"}

# 슬래시를 기준 삼아 뒤에 경로를 붙히면 페이지를 나누게 된다
# 현재 이건 items 뒤에 오는 값을 item_id 라는 이름으로
# 파라메타를 받겠다는 뜻
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

'''
HTTP 메소드 4가지(CRUD)
@app.get() -> 조회 
- 서버에 있는 데이터를 가져오라는 요청 

@app.post()
- 서버에 데이터를 등록하는 요청을 이용할 때 사용한다 
- 로그인, 글작성 등 중요 데이터를 서버로 보낼때 사용한다 
데이터가 주소창에 노출되지 않고 숨겨져서 전송된다 

@app.put() 
- 서버에 있는 데이터를 새로운 내용으로 변경할 때 사용함 

@app.delete()
- 서버의 데이터를 삭제하는 요청을 할 때 사용함 

/docs => fast api 의 자동 api 문서로 이동 ( 스웨거 )
'''
# 임시로 데이터베이스 역할을 할 파이썬 리스트
items_db = [
    {"item_id": 1, "name": "노트북", "price": 1500000},
    {"item_id": 2, "name": "마우스", "price": 50000},
    {"item_id": 3, "name": "키보드", "price": 120000},
    {"item_id": 4, "name": "모니터", "price": 350000},
    {"item_id": 5, "name": "아이패드", "price": 900000},
]

# 전체 상품 목록 조회
@app.get("/product")
async def all_products():
    return items_db

# 특정 상품 하나만 조회
@app.get("/product/{item_id}")
async def get_item(item_id: int):
    # 리스트를 순회하면서 사용자가 요청한 item_id 값과 일치하는 상품을 찾음
    for item in items_db:
        if item["item_id"] == item_id:
            return item;
    # 만약 찾지 못하면 상품을 찾을 수 없습니다라는 메시지를 날림
    raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.");

# 상품 등록
@app.post("/product/register")
async def create_item(item: Item):
    new_id = items_db[-1]["item_id"] + 1 if items_db else 1
    new_item = {"item_id": new_id, "name": item.name, "price": item.price}
    items_db.append(new_item)
    return {"message": "상품이 등록되었습니다.", "data": new_item}

# 상품 정보 삭제
@app.delete("/product/delete/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item["item_id"] == item.id:
            deleted_item = items_db.pop(index);
            return {"message": "상품이 삭제되었습니다.", "data": deleted_item}
    return HTTPException(status_code=404, detail="삭제할 상품을 찾을 수 없습니다.")

# 상품 정보 수정
@app.put("/product/{item_id}")
async def update_item(item_id: int, updated_item: Item):
    for item in items_db:
        if item["item_id"] == item_id:
            item["name"] = updated_item.name
            item["price"] = updated_item.price
            return {"message": "상품 정보가 수정되었습니다.", "data": item}

    raise HTTPException(status_code=404, detail="수정할 상품을 찾을 수 없습니다.")

# main 함수는 시작함수이다
# 즉 fast api 애플리케이션이 시작될 때 제일 먼저 실행되는 함수
# 다른 파일에서 이 파일을 불러올 때는 실행되지 않도록 방지
'''
import unicorn
- Fast API 서버를 구동하기 위해 필요한 ASGI 웹 서버인 Uvicorn 라이브러리를 불러온다 

127.0.0.1 => 로컬에서만 접속할 수 있게 한다 
port => 8000번 포트로 서버를 연다 
reload=True => 코드를 수정하고 저장만 하면 서버를 껏다 끌 필요없이 자동으로 
변경 사항을 반영해 준다 

127.0.0.1 == localhost
- 인터넷 상에 모든 컴퓨터는 자기만의 ip 주소를 가진다 그중 해당 ip 주소는 
지금 내가 쓰고 있는 이 컴퓨터를 가리키는 특수 주소이다 
외부에서는 내 애플리케이션에 접근할 수 없고 오직 내 컴퓨터에서만 접속할 수 있다 

port == 8000
- 컴퓨터 안에는 여러가지 수많은 프로그램이 작동하고 잇는데 
포트는 이 프로그램들이 데이터를 주고받을 전용 문이라고 보면된다 
즉) 배포를 하였을 때 인터넷을 통해 배포된 서버 ip로 접속을 하는데 
그 서버 컴퓨터에 실행되는 프로그램들 중 어디에 접속을 할 것인가 
한마디로 앞으로 제 애플리케이션에 들어올 클라이언트들께서는 8000번 
으로 들어오시면 됩니다 ~~ 

127.0.0.1:8000
- 내컴퓨터 127.0.0.1 이라는 집으로 찾아가서 8000번 문으로 
내 웹 서버 프로그램을 접속 

netstat -ano | findstr 8000
현재 내 컴퓨터에서 8000번 포트가 실행되고 있는지 확인하는 명령어 

uvicorn main:app  => fast api 실행 명령어 
'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True);