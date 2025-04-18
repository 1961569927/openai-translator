from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import requests
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = FastAPI()


@app.post("/process-pdf/")
async def process_pdf(
        pdf_file: UploadFile = File(..., description="PDF文件"),
        glm_model_url: str = Form(..., description="GLM模型服务URL")
):
    # 验证文件类型
    if pdf_file.content_type not in ["application/pdf", "application/octet-stream"]:
        raise HTTPException(400, detail="无效的文件类型，请上传PDF文件")

    try:
        # 读取并解析PDF内容
        pdf_content = await pdf_file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages])

        # 调用GLM模型服务
        model_response = requests.post(
            glm_model_url,
            json={"text": extracted_text},
            timeout=30
        )
        model_response.raise_for_status()
        processed_content = model_response.json().get("processed_text", "")

        # 生成新的PDF
        buffer = BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
        text = pdf_canvas.beginText(40, 750)
        text.setFont("Helvetica", 12)

        # 处理文本换行
        for line in processed_content.split('\n'):
            text.textLine(line)

        pdf_canvas.drawText(text)
        pdf_canvas.save()

        # 准备返回结果
        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=processed.pdf"}
        )

    except requests.RequestException as e:
        raise HTTPException(500, detail=f"模型服务调用失败: {str(e)}")
    except PyPDF2.errors.PdfReadError:
        raise HTTPException(400, detail="无效的PDF文件")
    except Exception as e:
        raise HTTPException(500, detail=f"服务器内部错误: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)