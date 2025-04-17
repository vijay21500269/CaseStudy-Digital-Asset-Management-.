from dao.asset_management_service_impl import AssetManagementServiceImpl
from myexceptions.asset_not_found_exception import AssetNotFoundException
from myexceptions.asset_not_maintain_exception import AssetNotMaintainException

if __name__ == "__main__":
    service = AssetManagementServiceImpl()

    try:
        asset_id = int(input("Enter Asset ID: "))
        asset = service.get_asset_by_id(asset_id)
        print("Asset Details:", asset)

        service.check_asset_maintenance(asset_id)
        print("Asset is properly maintained.")

    except AssetNotFoundException as e:
        print("Error:", e)

    except AssetNotMaintainException as e:
        print("Warning:", e)

    except Exception as e:
        print("Unexpected error:", e)
