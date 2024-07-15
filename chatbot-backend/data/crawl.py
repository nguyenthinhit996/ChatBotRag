from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader, DirectoryLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.schema import Document
import bs4

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=20,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

def process_files(file_path):
    file_types = ["*.pdf", "*.txt", "*.doc", "*.docx"]
    documents = []
    for file_type in file_types:
        loader = DirectoryLoader(
            file_path,
            glob=file_type,
            loader_cls=UnstructuredFileLoader
        )
        documents.extend(loader.load())
    return documents

def process_web(urls):
    web_loader = WebBaseLoader(
        web_paths=urls,
         bs_kwargs=dict(
            # No parse_only argument, which means it will parse the entire HTML content
        ),
    )
    return web_loader.load()

def create_combined_db(text=None, file_path=None, urls=None, vector_db_path="vectorstores/db_faiss", model_name="all-MiniLM-L6-v2.gguf2.f16.gguf"):
    documents = []

    # Assuming GPT4AllEmbeddings takes model_name as a parameter
    model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
    gpt4all_kwargs = {'allow_download': 'True'}
    embedding_model = GPT4AllEmbeddings(
        model_name=model_name,
        gpt4all_kwargs=gpt4all_kwargs
    )

    try:
        if text:
            documents.extend(process_text(text))
            print(f"Processed text: {len(documents)} documents added.")

        if file_path:
            documents.extend(process_files(file_path))
            print(f"Processed files: {len(documents)} documents added.")

        if urls:
            documents.extend(process_web(urls))
            print(f"Processed URLs: {len(documents)} documents added.")
    except Exception as e:
        print(f"Error processing input: {e}")
        raise

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks.")
    except Exception as e:
        print(f"Error splitting documents: {e}")
        raise

    try:
        if model_name is None or not isinstance(model_name, str):
            raise ValueError("Invalid model_name provided.")

        # embedding_model = GPT4AllEmbeddings(model_name=model_name)
        db = FAISS.from_documents(chunks, embedding_model)
        db.save_local(vector_db_path)
        print(f"Vector database saved at {vector_db_path}.")
    except Exception as e:
        print(f"Error creating or saving FAISS database: {e}")
        raise

    return db

# Example usage:
pdf_data_path = "/content/drive/MyDrive/2024/rag/data-public"
vector_db_path = "./db_faiss"
urls_common = [
    "https://resvu.io",
    "https://resvu.io/request-demo/",
    "https://resvu.io/login/",
    "https://console.communitilink.com.au/",
    "https://buildingportal.communitilink.com.au/auth/login",
    "https://console.fmlink.com.au/auth",
    "https://www.strata.community/",
    "https://www.stratamax.com/",
    "https://www.propertyiq.com.au/",
    "https://www.caionline.org/pages/default.aspx",
    "https://tssmarketing.vmsclientonline.com/",
    "https://resvu.io/about/",
    "https://resvu.io/platform/",
    "https://resvu.io/privacy/",
    "https://resvu.io/terms-and-conditions/",
    "https://help.resvu.com.au/en/",
    "https://resvu.io/resvu-wins-scaq-excellence-in-service-award/",
    "https://www.facebook.com/resvusoftware",
    "https://www.linkedin.com/company/resvu",
    "https://www.instagram.com/resvu.io/",
    "https://resvu.io/news/",
    "https://resvu.io/contact/"
    "https://help.resvu.com.au/en/collections/2674914-company-dashboard",
    "https://help.resvu.com.au/en/collections/2674915-community-site-console",
    "https://help.resvu.com.au/en/collections/2674923-resident-application",
    "https://help.resvu.com.au/en/collections/3861616-training-videos",
    "https://help.resvu.com.au/en/collections/2674916-facilities-management",
    "https://help.resvu.com.au/en/collections/3202472-inspection-app",
    "https://help.resvu.com.au/en/collections/4032741-webinars"
]


url_support_company_dashboard = [
    "https://help.resvu.com.au/en/articles/6021398-setting-the-site-manager-for-filtering-of-my-portfolio",
    "https://help.resvu.com.au/en/articles/6083041-resending-invite-email-through-company-dashboard",
    "https://help.resvu.com.au/en/articles/5976663-bulk-importing-sites-via-csv",
    "https://help.resvu.com.au/en/articles/4709347-creating-a-new-site",
    "https://help.resvu.com.au/en/articles/5758826-grouping-your-sites",
    "https://help.resvu.com.au/en/articles/4709344-site-codes",
    "https://help.resvu.com.au/en/articles/4709346-assign-an-admin-to-another-site",
    "https://help.resvu.com.au/en/articles/4914533-add-existing-residents-to-a-site",
    "https://help.resvu.com.au/en/articles/4783983-different-users-types-explained",
    "https://help.resvu.com.au/en/articles/4784009-bulk-site-updates",
    "https://help.resvu.com.au/en/collections/2702416-engagement",
    "https://help.resvu.com.au/en/articles/4784038-multi-site-communications",
    "https://help.resvu.com.au/en/collections/2702418-integrations",
    "https://help.resvu.com.au/en/articles/5641703-strata-max-api-integration-overview",
    "https://help.resvu.com.au/en/articles/5732494-strata-max-lot-owner-benefits-mobile",
    "https://help.resvu.com.au/en/articles/5648189-propertyiq-integration-overview",
    "https://help.resvu.com.au/en/articles/5732515-propertyiq-lot-owner-benefits-mobile",
    "https://help.resvu.com.au/en/articles/8098610-propertyiq-integration-faqs",
    "https://help.resvu.com.au/en/articles/8098611-strata-max-integration-faqs",
    "https://help.resvu.com.au/en/collections/3769303-first-time-setup",
    "https://help.resvu.com.au/en/articles/6829175-company-dashboard-setup-examples"
]

url_support_community_site_console = [
    "https://help.resvu.com.au/en/collections/2702392-communication",
    "https://help.resvu.com.au/en/articles/4709395-creating-an-alert",
    "https://help.resvu.com.au/en/articles/4709394-creating-a-new-notice",
    "https://help.resvu.com.au/en/articles/5719146-creating-a-newsletter",
    "https://help.resvu.com.au/en/articles/5719286-creating-policies-procedures-communication",
    "https://help.resvu.com.au/en/articles/4709389-create-managing-a-survey",
    "https://help.resvu.com.au/en/articles/5719534-creating-communication-templates",
    "https://help.resvu.com.au/en/collections/2702399-user-management",
    "https://help.resvu.com.au/en/articles/4709353-inviting-other-admins",
    "https://help.resvu.com.au/en/articles/4773743-help-your-residents-signup",
    "https://help.resvu.com.au/en/articles/4709392-manually-add-a-user",
    "https://help.resvu.com.au/en/articles/4709355-bulk-importing-users-into-your-site",
    "https://help.resvu.com.au/en/articles/4709390-managing-user-groups",
    "https://help.resvu.com.au/en/articles/4824666-permission-management",
    "https://help.resvu.com.au/en/collections/2702398-requests",
    "https://help.resvu.com.au/en/articles/6829169-creating-form-templates",
    "https://help.resvu.com.au/en/articles/7548590-managing-form-submissions",
    "https://help.resvu.com.au/en/collections/2702408-files-site-information",
    "https://help.resvu.com.au/en/articles/5808587-adding-sustainability-options",
    "https://help.resvu.com.au/en/articles/5722490-adding-site-amenity-information",
    "https://help.resvu.com.au/en/articles/5722448-adding-current-activities",
    "https://help.resvu.com.au/en/articles/4709387-adding-connection-information",
    "https://help.resvu.com.au/en/articles/4709386-managing-useful-links",
    "https://help.resvu.com.au/en/articles/4709385-adding-important-site-contacts",
    "https://help.resvu.com.au/en/articles/4709388-using-the-file-browser",
    "https://help.resvu.com.au/en/articles/4709360-custom-sections",
    "https://help.resvu.com.au/en/collections/2702400-concierge",
    "https://help.resvu.com.au/en/articles/5890708-your-local-deals",
    "https://help.resvu.com.au/en/articles/4709381-venues-and-amenities",
    "https://help.resvu.com.au/en/articles/5670757-using-groups-to-allow-specific-users-to-see-venues",
    "https://help.resvu.com.au/en/articles/4709379-delivery-management",
    "https://help.resvu.com.au/en/articles/4709384-venue-bookings",
    "https://help.resvu.com.au/en/articles/4709366-digital-noticeboard-settings",
    "https://help.resvu.com.au/en/articles/4709377-personal-reminders",
    "https://help.resvu.com.au/en/collections/2702394-residenthub",
    "https://help.resvu.com.au/en/articles/5808698-community-wall-blocked-users",
    "https://help.resvu.com.au/en/articles/5808684-create-a-social-club",
    "https://help.resvu.com.au/en/articles/4914197-resident-requesting-a-social-club-then-admin-creates-social-club",
    "https://help.resvu.com.au/en/articles/4914193-creating-events",
    "https://help.resvu.com.au/en/articles/4709348-creating-a-community-wall",
    "https://help.resvu.com.au/en/collections/2702403-committee-board-hub",
    "https://help.resvu.com.au/en/articles/5809015-resident-committee-board-requests",
    "https://help.resvu.com.au/en/articles/5808885-invoice-approvals",
    "https://help.resvu.com.au/en/articles/5808706-managing-active-topics",
    "https://help.resvu.com.au/en/articles/4709356-assigning-members-to-committee-board-hub",
    "https://help.resvu.com.au/en/collections/2702407-settings",
    "https://help.resvu.com.au/en/articles/5816477-custom-app-section",
    "https://help.resvu.com.au/en/articles/5816387-email-signature",
    "https://help.resvu.com.au/en/articles/5816250-payment-settings",
    "https://help.resvu.com.au/en/articles/5816210-venue-settings",
    "https://help.resvu.com.au/en/articles/5809197-custom-report-header",
    "https://help.resvu.com.au/en/articles/5809164-turning-on-off-the-application-features",
    "https://help.resvu.com.au/en/articles/5809145-admin-tasks",
    "https://help.resvu.com.au/en/articles/5752367-upload-a-site-image",
    "https://help.resvu.com.au/en/articles/4709362-setting-up-admin-notifications",
    "https://help.resvu.com.au/en/articles/4709367-general-site-settings",
    "https://help.resvu.com.au/en/articles/4709361-admin-user-profile",
    "https://help.resvu.com.au/en/collections/2702404-frequently-asked-questions",
    "https://help.resvu.com.au/en/articles/6013757-did-my-communication-go-out",
    "https://help.resvu.com.au/en/articles/7915678-site-setup-examples",
    "https://help.resvu.com.au/en/articles/6021386-menu-badges",
    "https://help.resvu.com.au/en/articles/5983917-where-is-the-site-code-in-the-site-admin-portal",
    "https://help.resvu.com.au/en/articles/4709396-what-is-a-push-notification",
    "https://help.resvu.com.au/en/articles/4709391-understanding-your-dashboard",
    "https://help.resvu.com.au/en/collections/3769302-submission-management",
    "https://help.resvu.com.au/en/articles/5795828-my-portfolio-popup",
    "https://help.resvu.com.au/en/articles/7065665-managers-dashboard"
]

url_support_resident_application = [
    "https://help.resvu.com.au/en/collections/2760877-registration",
    "https://help.resvu.com.au/en/articles/4889889-account-approval-process",
    "https://help.resvu.com.au/en/articles/4709349-your-site-code-explained",
    "https://help.resvu.com.au/en/articles/4877405-i-m-a-part-of-multiple-sites",
    "https://help.resvu.com.au/en/collections/2760880-authentication",
    "https://help.resvu.com.au/en/articles/4709382-i-m-having-trouble-logging-in",
    "https://help.resvu.com.au/en/articles/4882831-i-m-having-password-issues",
    "https://help.resvu.com.au/en/articles/4877402-how-do-i-logout-of-the-application",
    "https://help.resvu.com.au/en/collections/2760890-profile",
    "https://help.resvu.com.au/en/articles/4709369-changing-account-details",
    "https://help.resvu.com.au/en/articles/4709350-how-to-unsubscribe-from-emails",
    "https://help.resvu.com.au/en/collections/3210447-communications",
    "https://help.resvu.com.au/en/articles/4709359-viewing-alerts",
    "https://help.resvu.com.au/en/articles/4709374-respond-to-a-survey",
    "https://help.resvu.com.au/en/articles/5716149-viewing-current-activities",
    "https://help.resvu.com.au/en/articles/4709372-viewing-notices",
    "https://help.resvu.com.au/en/articles/5716165-viewing-newsletters",
    "https://help.resvu.com.au/en/articles/5716210-viewing-policy-procedures",
    "https://help.resvu.com.au/en/articles/5716226-viewing-site-files",
    "https://help.resvu.com.au/en/collections/3210421-requests",
    "https://help.resvu.com.au/en/articles/5715778-view-submitted-common-area-maintenance-requests-by-other-users",
    "https://help.resvu.com.au/en/articles/6829172-how-a-resident-submits-a-form-through-the-phone-app",
    "https://help.resvu.com.au/en/articles/4709376-submitting-a-maintenance-request-through-the-app",
    "https://help.resvu.com.au/en/articles/5712371-submitting-a-committee-board-request",
    "https://help.resvu.com.au/en/articles/5715818-view-the-status-of-your-maintenance-requests",
    "https://help.resvu.com.au/en/collections/3210615-amenities",
    "https://help.resvu.com.au/en/articles/5716402-viewing-amenity-rules",
    "https://help.resvu.com.au/en/articles/5716399-viewing-your-booked-amenities",
    "https://help.resvu.com.au/en/articles/5716373-confirming-a-booked-amenity",
    "https://help.resvu.com.au/en/articles/5716371-booking-an-amenity",
    "https://help.resvu.com.au/en/collections/3210567-site-information",
    "https://help.resvu.com.au/en/articles/5716270-viewing-site-connection-information",
    "https://help.resvu.com.au/en/articles/5716254-viewing-site-contact-information",
    "https://help.resvu.com.au/en/articles/5716318-viewing-site-useful-links",
    "https://help.resvu.com.au/en/articles/5716339-viewing-site-amenity-information",
    "https://help.resvu.com.au/en/articles/5716358-viewing-site-sustainability-information",
    "https://help.resvu.com.au/en/collections/3208757-resident-hub",
    "https://help.resvu.com.au/en/articles/5712708-post-a-message-in-a-social-club",
    "https://help.resvu.com.au/en/articles/5712683-join-a-social-club",
    "https://help.resvu.com.au/en/articles/5712481-request-a-social-club",
    "https://help.resvu.com.au/en/articles/5712463-view-an-upcoming-event",
    "https://help.resvu.com.au/en/articles/5712453-reply-to-a-message-in-the-community-wall",
    "https://help.resvu.com.au/en/articles/5712449-post-a-message-to-the-community-wall",
    "https://help.resvu.com.au/en/collections/3208745-committee-board-hub",
    "https://help.resvu.com.au/en/articles/5712387-creating-a-new-committee-board-topic",
    "https://help.resvu.com.au/en/articles/5712421-committee-board-group-approvals",
    "https://help.resvu.com.au/en/articles/5712412-responding-to-a-committee-board-topic",
    "https://help.resvu.com.au/en/articles/5712408-updating-a-resident-committee-board-request",
    "https://help.resvu.com.au/en/collections/2760889-features",
    "https://help.resvu.com.au/en/articles/5716441-changing-between-sites-once-logged-in",
    "https://help.resvu.com.au/en/articles/5716430-view-your-deliveries",
    "https://help.resvu.com.au/en/collections/3218472-myhome-lot-owner-integration",
    "https://help.resvu.com.au/en/articles/5702525-myhome-resident-app-stratamax",
    "https://help.resvu.com.au/en/articles/5702835-myhome-resident-app-property-iq",
    "https://help.resvu.com.au/en/collections/2760895-frequently-asked-questions",
    "https://help.resvu.com.au/en/articles/4709383-why-can-t-i-view-my-document-on-a-computer-mac-windows"
]

url_support_facilities_management = [
    "https://help.resvu.com.au/en/articles/5316119-account-management-account-users",
    "https://help.resvu.com.au/en/articles/5694461-importing-sites-and-contractors-in-account-dashboard-for-fm-link",
    "https://help.resvu.com.au/en/collections/2989480-site-settings",
    "https://help.resvu.com.au/en/articles/4709401-setting-up-your-building",
    "https://help.resvu.com.au/en/articles/4709364-report-headers",
    "https://help.resvu.com.au/en/articles/5684843-tag-lists-settings-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989846-inspection-templates-inspector",
    "https://help.resvu.com.au/en/articles/5699517-complete-a-site-inspection-in-fm-link",
    "https://help.resvu.com.au/en/articles/5696733-create-a-site-inspection-template-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989486-file-browser",
    "https://help.resvu.com.au/en/articles/5687950-file-browser-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989858-requests",
    "https://help.resvu.com.au/en/articles/5681532-invoice-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5681331-create-quote-request-in-fm-link",
    "https://help.resvu.com.au/en/articles/5694142-add-scheduled-maintenance-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678695-manage-work-order-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678062-creating-a-maintenance-request-in-fm-link",
    "https://help.resvu.com.au/en/articles/5684376-manage-resident-defect-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678234-create-work-order-in-fm-link",
    "https://help.resvu.com.au/en/articles/5681411-manage-quote-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5684350-manage-resident-maintenance-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678153-manage-maintenance-requests-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989864-registers",
    "https://help.resvu.com.au/en/articles/5694031-create-assets-in-fm-link",
    "https://help.resvu.com.au/en/articles/5694091-manage-access-key-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989871-users",
    "https://help.resvu.com.au/en/articles/5316055-contractors",
    "https://help.resvu.com.au/en/articles/5694326-creating-contractors-in-fm-link",
    "https://help.resvu.com.au/en/collections/3246835-app-settings",
    "https://help.resvu.com.au/en/articles/5788725-global-contractor-management"
]

url_support_inspection_app = [
    "https://help.resvu.com.au/en/articles/5316119-account-management-account-users",
    "https://help.resvu.com.au/en/articles/5694461-importing-sites-and-contractors-in-account-dashboard-for-fm-link",
    "https://help.resvu.com.au/en/collections/2989480-site-settings",
    "https://help.resvu.com.au/en/articles/4709401-setting-up-your-building",
    "https://help.resvu.com.au/en/articles/4709364-report-headers",
    "https://help.resvu.com.au/en/articles/5684843-tag-lists-settings-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989846-inspection-templates-inspector",
    "https://help.resvu.com.au/en/articles/5699517-complete-a-site-inspection-in-fm-link",
    "https://help.resvu.com.au/en/articles/5696733-create-a-site-inspection-template-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989486-file-browser",
    "https://help.resvu.com.au/en/articles/5687950-file-browser-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989858-requests",
    "https://help.resvu.com.au/en/articles/5681532-invoice-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5681331-create-quote-request-in-fm-link",
    "https://help.resvu.com.au/en/articles/5694142-add-scheduled-maintenance-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678695-manage-work-order-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678062-creating-a-maintenance-request-in-fm-link",
    "https://help.resvu.com.au/en/articles/5684376-manage-resident-defect-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678234-create-work-order-in-fm-link",
    "https://help.resvu.com.au/en/articles/5681411-manage-quote-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5684350-manage-resident-maintenance-requests-in-fm-link",
    "https://help.resvu.com.au/en/articles/5678153-manage-maintenance-requests-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989864-registers",
    "https://help.resvu.com.au/en/articles/5694031-create-assets-in-fm-link",
    "https://help.resvu.com.au/en/articles/5694091-manage-access-key-in-fm-link",
    "https://help.resvu.com.au/en/collections/2989871-users",
    "https://help.resvu.com.au/en/articles/5316055-contractors",
    "https://help.resvu.com.au/en/articles/5694326-creating-contractors-in-fm-link",
    "https://help.resvu.com.au/en/collections/3246835-app-settings",
    "https://help.resvu.com.au/en/articles/5788725-global-contractor-management",
]

all_url = urls_common + url_support_company_dashboard + url_support_community_site_console + url_support_resident_application + url_support_facilities_management + url_support_inspection_app


raw_text = """
Thinh created you who is a chatbox at Resvu,
"""

# Create combined DB from all sources
# create_combined_db(text=raw_text, file_path=pdf_data_path, urls=all_url, vector_db_path=vector_db_path)